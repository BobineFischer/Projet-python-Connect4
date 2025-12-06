import numpy as np
import time
import random

class Agent:
    def __init__(self, env=None, player_name=None):
        self.rows = 6
        self.cols = 7
        
        # --- 1. Gestion du Temps (Stratégie de sécurité) ---
        self.total_time_bank = 0 
        # Temps de base réduit pour anticiper la latence du serveur ou le GC
        self.base_time = 1.95    
        
        # --- 2. Structures de données ---
        # Taille de la table de transposition limitée à 5M pour éviter 
        # les pics de latence dus au Garbage Collector de Python
        self.tt = {} 
        self.max_tt_size = 5000000 
        
        self.endgame_db = {}
        
        # --- 3. Heuristiques ---
        self.killers = [[None] * 2 for _ in range(50)]
        self.history = [0] * 7
        
        self.init_bitboards()
        self.init_opening_book()

    def init_bitboards(self):
        """Initialisation des masques binaires (Bitboards)"""
        self.top_mask_col = [(1 << (5 + c * 7)) for c in range(7)]
        self.col_mask = [((1 << 6) - 1) << (c * 7) for c in range(7)]
        self.bottom_mask_col = [(1 << (c * 7)) for c in range(7)]
        self.mask_col3 = 0
        for r in range(6): self.mask_col3 |= (1 << (3 * 7 + r))

    def init_opening_book(self):
        """Chargement de la bibliothèque d'ouvertures"""
        self.book = {}
        openings = {
            "": 3, "4": 3, 
            "1": 3, "2": 3, "3": 3, "5": 3, "6": 3, "7": 3,
            "44": 3, "43": 3, "45": 3,
            "444": 2, "4444": 2, "44444": 2,
            "434": 2, "33": 3, "333": 3, "22": 3,
            "34": 3, "24": 3, "54": 3, "64": 3
        }
        for seq, action in openings.items():
            moves = [int(char) - 1 for char in seq]
            p1, p2, occupied, heights, valid = 0, 0, 0, [0]*7, True
            for i, col in enumerate(moves):
                if heights[col] >= 6: valid = False; break
                bit = 1 << (col * 7 + heights[col])
                occupied |= bit
                if i % 2 == 0: p1 |= bit
                else: p2 |= bit
                heights[col] += 1
            if not valid: continue
            my_mask = p1 if len(moves) % 2 == 0 else p2
            self.book[(occupied, my_mask)] = action

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        start_time = time.time()
        
        # --- 1. Analyse de l'observation (Correction gravité) ---
        if isinstance(observation, dict) and 'observation' in observation:
            obs_data = observation['observation']
        else:
            obs_data = observation
        
        position = 0 
        mask = 0     
        for c in range(7):
            col_base = c * 7
            for r in range(6):
                if obs_data[r, c, 0] == 1:
                    bit = 1 << (col_base + (5 - r)) 
                    position |= bit
                    mask |= bit
                elif obs_data[r, c, 1] == 1:
                    position |= (1 << (col_base + (5 - r)))

        # --- 2. Détermination du joueur (P1/P2) ---
        move_count = self.count_set_bits(position)
        self.is_p1 = (move_count % 2 == 0)

        # --- 3. Consultation du livre d'ouvertures ---
        if (position, mask) in self.book: return self.book[(position, mask)]
        if move_count == 0: return 3
        if move_count == 1:
             center_mask = ((1<<6)-1) << 21
             if not (position & center_mask): return 3

        if (position, mask) in self.endgame_db:
            score, saved_move = self.endgame_db[(position, mask)]
            if score > -9000: return saved_move

        # --- 4. Coups légaux ---
        if action_mask is not None:
            legal_moves = [i for i, v in enumerate(action_mask) if v == 1]
        else:
            legal_moves = [c for c in range(7) if (position & self.top_mask_col[c]) == 0]
        if not legal_moves: return 0 
        if len(legal_moves) == 1: return legal_moves[0]

        # --- 5. Contrôle strict du budget temps ---
        time_budget = self.base_time
        if self.total_time_bank > 0.5:
            # Plafond absolu à 2.40s. On garde 0.6s de marge pour la stabilité système.
            time_budget = min(2.40, self.base_time + self.total_time_bank * 0.4)
        
        # Nettoyage préventif si la table est trop grosse
        if len(self.tt) > self.max_tt_size: self.tt = {}

        best_move = random.choice(legal_moves)
        
        try:
            # A. Vérification de victoire immédiate
            forced = self.solve_immediate(position, mask, legal_moves)
            if forced is not None: 
                # On économise le temps non utilisé
                self.total_time_bank += (time_budget - (time.time() - start_time))
                return forced

            # B. Recherche PVS (Principal Variation Search)
            remaining_moves = 42 - move_count
            is_endgame = remaining_moves <= 18
            
            moves = self.sort_moves(position, mask, legal_moves, 0)
            best_move = moves[0]

            max_depth = remaining_moves
            start_depth = 1
            if is_endgame: start_depth = max(1, remaining_moves - 8)

            for depth in range(start_depth, max_depth + 1):
                # Vérification du chrono avant nouvelle itération
                if time.time() - start_time > time_budget: break
                
                window = 20000
                if depth > 6: window = 150 
                
                score = self.pvs(position, mask, depth, -window, window, start_time, time_budget)
                
                if (position, mask) in self.tt:
                    cand = self.tt[(position, mask)][2]
                    if cand in legal_moves: best_move = cand
                
                if score >= 9000: 
                    self.endgame_db[(position, mask)] = (score, best_move)
                    break 
                if depth >= remaining_moves and abs(score) < 9000:
                    self.endgame_db[(position, mask)] = (score, best_move)
                    break

        except Exception:
            pass # En cas de timeout, on retourne le meilleur coup trouvé
        
        # Mise à jour de la banque de temps
        used_time = time.time() - start_time
        if used_time < time_budget:
            # On stocke une partie du temps gagné (coeff 0.8)
            self.total_time_bank += (time_budget - used_time) * 0.8
        else:
            self.total_time_bank = 0
            
        return best_move

    def pvs(self, position, mask, depth, alpha, beta, start_time, time_limit):
        # Contrôle fréquent du temps (tous les 511 noeuds)
        # Permet de stopper rapidement même dans les branches profondes
        if (mask & 511 == 0):
            if time.time() - start_time > time_limit: raise TimeoutError()

        key = (position, mask)
        if key in self.endgame_db: return self.endgame_db[key][0]

        tt_entry = self.tt.get(key)
        if tt_entry and tt_entry[0] >= depth:
            if tt_entry[3] == 0: return tt_entry[1] 
            elif tt_entry[3] == 1: alpha = max(alpha, tt_entry[1])
            elif tt_entry[3] == 2: beta = min(beta, tt_entry[1])
            if alpha >= beta: return tt_entry[1]

        opponent_mask = position ^ mask
        if self.check_win_bitboard(opponent_mask): return -10000 - depth 

        if depth == 0: 
            return self.evaluate_anti_ai(position, mask)
            
        if position & 0x3FFFFFFFFFF == 0x3FFFFFFFFFF: return 0

        moves_list = [c for c in [3, 2, 4, 1, 5, 0, 6] if (position & self.top_mask_col[c]) == 0]
        tt_move = tt_entry[2] if tt_entry else None
        sorted_moves = self.sort_moves(position, mask, moves_list, depth, tt_move)
        
        best_score = -20000
        best_move = sorted_moves[0]
        
        for i, col in enumerate(sorted_moves):
            move_bit = (position + (1 << (col * 7))) & self.col_mask[col]
            new_pos = position | move_bit
            
            if i == 0:
                score = -self.pvs(new_pos, opponent_mask, depth - 1, -beta, -alpha, start_time, time_limit)
            else:
                score = -self.pvs(new_pos, opponent_mask, depth - 1, -alpha - 1, -alpha, start_time, time_limit)
                if alpha < score < beta:
                    score = -self.pvs(new_pos, opponent_mask, depth - 1, -beta, -score, start_time, time_limit)
            
            if score > best_score:
                best_score = score
                best_move = col
            
            alpha = max(alpha, score)
            if alpha >= beta:
                if col != best_move:
                    self.update_killers(depth, col)
                    self.history[col] += depth * depth
                break 

        flag = 0 
        if best_score <= alpha: flag = 2 
        elif best_score >= beta: flag = 1 
        
        if not tt_entry or depth >= tt_entry[0]:
            self.tt[key] = (depth, best_score, best_move, flag)
        
        if best_score > 9000 or best_score < -9000:
             self.endgame_db[key] = (best_score, best_move)

        return best_score

    def evaluate_anti_ai(self, position, mask):
        opp_mask = position ^ mask
        score = 0
        
        m_col3 = mask >> 21 & 0x3F; o_col3 = opp_mask >> 21 & 0x3F
        score += (m_col3.bit_count() * 7 - o_col3.bit_count() * 7)
        
        m_col24 = (mask >> 14 & 0x3F) | (mask >> 28 & 0x3F)
        o_col24 = (opp_mask >> 14 & 0x3F) | (opp_mask >> 28 & 0x3F)
        score += (m_col24.bit_count() * 4 - o_col24.bit_count() * 4)

        even_mask = 0
        for c in range(7): even_mask |= (0x15 << (c*7))
        
        my_pieces_even = (mask & even_mask).bit_count()
        my_pieces_odd = (mask & (~even_mask)).bit_count()
        
        if self.is_p1: score += my_pieces_even * 2
        else: score += my_pieces_odd * 2

        m = mask
        h_3 = (m & (m >> 7) & (m >> 14)) 
        score += h_3.bit_count() * 8 
        m_h = (m & (m >> 1)) & (m >> 2) 
        score += m_h.bit_count() * 5
        
        o = opp_mask
        o_3 = (o & (o >> 7) & (o >> 14))
        score -= o_3.bit_count() * 10 
        o_h = (o & (o >> 1)) & (o >> 2)
        score -= o_h.bit_count() * 6

        return score

    def sort_moves(self, position, mask, legal_moves, depth, tt_move=None):
        if len(legal_moves) <= 1: return legal_moves
        scores = {}
        for m in legal_moves:
            score = 0
            if m == tt_move: score += 1000000
            elif self.killers[depth][0] == m: score += 500000
            elif self.killers[depth][1] == m: score += 400000
            score += self.history[m]
            if m == 3: score += 80
            elif m == 2 or m == 4: score += 40
            elif m == 1 or m == 5: score += 20
            if m == 0 or m == 6: score -= 15 
            scores[m] = score
        return sorted(legal_moves, key=lambda x: scores[x], reverse=True)

    def update_killers(self, depth, move):
        if self.killers[depth][0] != move:
            self.killers[depth][1] = self.killers[depth][0]
            self.killers[depth][0] = move

    def solve_immediate(self, position, mask, legal_moves):
        opp_mask = position ^ mask
        for col in legal_moves:
            move_bit = (position + (1 << (col * 7))) & self.col_mask[col]
            if self.check_win_bitboard(mask | move_bit): return col
        block_move = None
        for col in legal_moves:
            move_bit = (position + (1 << (col * 7))) & self.col_mask[col]
            if self.check_win_bitboard(opp_mask | move_bit):
                block_move = col
                break 
        if block_move is not None: return block_move
        return None

    def check_win_bitboard(self, bitboard):
        m = bitboard & (bitboard >> 1); 
        if m & (m >> 2): return True
        m = bitboard & (bitboard >> 7); 
        if m & (m >> 14): return True
        m = bitboard & (bitboard >> 6); 
        if m & (m >> 12): return True
        m = bitboard & (bitboard >> 8); 
        if m & (m >> 16): return True
        return False
    
    def count_set_bits(self, n):
        try: return n.bit_count()
        except AttributeError: return bin(n).count('1')