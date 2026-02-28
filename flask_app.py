from flask import Flask, render_template, request, session
import json
import random

app = Flask(__name__)
app.secret_key = 'chess_magic_key'

# --- LOAD DATABASE ---
def load_players():
    try:
        with open('/home/nyx369/mysite/players.json', 'r') as f:
            return json.load(f)
    except:
        return []

# --- 20 HINTS (QUESTIONS) ---
ALL_QUESTIONS = [
    {"key": "is_alive", "text": "Is the player currently alive?"},
    {"key": "is_female", "text": "Is the player female?"},
    {"key": "is_active", "text": "Is the player currently active in top-level chess?"},
    {"key": "is_retired", "text": "Has the player officially retired?"},
    {"key": "is_world_champion", "text": "Was or is the player a Classical World Champion?"},
    {"key": "is_russian", "text": "Is the player from Russia (or Soviet Union)?"},
    {"key": "is_american", "text": "Is the player from the USA?"},
    {"key": "is_indian", "text": "Is the player from India?"},
    {"key": "is_chinese", "text": "Is the player from China?"},
    {"key": "is_european", "text": "Is the player from Europe (excluding Russia)?"},
    {"key": "plays_aggressive", "text": "Is the player known for an aggressive, attacking style?"},
    {"key": "plays_positional", "text": "Is the player known for a solid, positional style?"},
    {"key": "is_theory_expert", "text": "Is the player famous for deep opening preparation?"},
    {"key": "plays_london_system", "text": "Is the player famous for playing the London System?"},
    {"key": "plays_kings_indian", "text": "Is the player famous for the King's Indian Defense?"},
    {"key": "is_endgame_specialist", "text": "Is the player renowned for endgame skills?"},
    {"key": "is_legend", "text": "Is the player considered a historical legend (pre-2000 peak)?"},
    {"key": "is_prodigy", "text": "Was the player a child prodigy (GM very young)?"},
    {"key": "is_2800", "text": "Has the player ever reached a rating of 2800+?"},
    {"key": "is_challenger", "text": "Did the player play for the World Championship but lose?"},
    {"key": "is_speed_demon", "text": "Is the player famous for speed chess (Blitz/Bullet)?"},
    {"key": "is_olympiad_winner", "text": "Has the player won a Gold medal at the Chess Olympiad?"},
    {"key": "is_streamer", "text": "Is the player a famous streamer/YouTuber?"},
    {"key": "is_commentator", "text": "Is the player well-known as a commentator?"},
    {"key": "has_written_books", "text": "Has the player written famous chess books?"},
    {"key": "is_coach", "text": "Is the player a famous coach?"},
    {"key": "has_course", "text": "Does the player have popular chess courses?"},
    {"key": "wears_glasses", "text": "Does the player wear glasses?"},
    {"key": "is_young", "text": "Is the player under 30 years old?"},
    {"key": "is_old", "text": "Is the player over 60 years old?"},
    {"key": "has_beard", "text": "Does the player have a beard or facial hair?"},
    {"key": "is_bald", "text": "Is the player bald?"},
    {"key": "is_married", "text": "Is the player known to be married?"},
    {"key": "has_siblings_in_chess", "text": "Does the player have siblings who are also chess masters?"},
    {"key": "has_controversy", "text": "Is the player associated with a major controversy?"},
    {"key": "is_criminal", "text": "Has the player had serious legal/criminal issues?"},
    {"key": "changed_federation", "text": "Did the player change their national federation?"},
    {"key": "played_machines", "text": "Did the player play a famous match against a computer?"},
    {"key": "is_computer_cheater", "text": "Has the player been accused of online cheating?"},
    {"key": "is_communist", "text": "Was the player a known Communist or Soviet loyalist?"},
    {"key": "is_political", "text": "Is the player active in politics?"},
    {"key": "beat_magnus", "text": "Has the player beaten Magnus Carlsen in a classical game?"},
    {"key": "crossed_2700", "text": "Has the player crossed the 2700 rating barrier?"},
    {"key": "is_rapid_champion", "text": "Has the player won a World Rapid or Blitz title?"},
    {"key": "is_candidate", "text": "Has the player competed in the Candidates Tournament?"},
    {"key": "is_online_champion", "text": "Has the player won a major online tournament?"},
    {"key": "is_chess960_champion", "text": "Is the player a Chess960 (Fischer Random) champion?"},
    {"key": "is_engine_developer", "text": "Did the player help develop chess engines?"},
    {"key": "is_arbiter", "text": "Is the player also a famous Arbiter?"},
    {"key": "is_fide_official", "text": "Does the player hold a position in FIDE?"}
]

@app.route('/')
def index():
    # AUTO-START: No button needed anymore!
    session['answers'] = {}
    session['q_order'] = random.sample(ALL_QUESTIONS, 15)
    session['q_index'] = 0
    first_q = session['q_order'][0]
    return render_template('index.html', state='question', question=first_q)

@app.route('/start')
def start_game():
    session['answers'] = {}
    session['q_order'] = random.sample(ALL_QUESTIONS, 15)
    session['q_index'] = 0
    first_q = session['q_order'][0]
    return render_template('index.html', state='question', question=first_q)





@app.route('/answer', methods=['POST'])
def answer():
    ans = request.form['choice']
    q_idx = session['q_index']
    q_list = session['q_order']

    # Save the answer
    current_key = q_list[q_idx]['key']
    session['answers'][current_key] = ans
    session['q_index'] += 1

    # --- SMART FILTERING ---
    players = load_players()
    possible_players = []

    for p in players:
        match = True
        for key, user_ans in session['answers'].items():
            # If user said "Don't Know", skip this check!
            if user_ans == "dont_know":
                continue

            # Compare stats (if data is missing, assume "no")
            player_stat = p['stats'].get(key, "no")
            if player_stat != user_ans:
                match = False
                break

        if match:
            possible_players.append(p)

    # WIN CONDITION
    if len(possible_players) == 1:
        return render_template('index.html', state='guess', player=possible_players[0])

    # LOSE CONDITION (0 candidates)
    if len(possible_players) == 0:
        return render_template('index.html', state='rare')

    # OUT OF QUESTIONS
    if session['q_index'] >= len(q_list):
        if len(possible_players) > 0:
             return render_template('index.html', state='guess', player=possible_players[0])
        else:
             return render_template('index.html', state='rare')

    # NEXT QUESTION
    next_q = q_list[session['q_index']]
    return render_template('index.html', state='question', question=next_q)

    # No one matches anymore? Show Mystery.
    if len(possible_players) == 0:
        return render_template('index.html', state='rare')

    # End of questions? Guess the best fit.
    if session['q_index'] >= len(q_list):
        return calculate_winner()

    next_q = q_list[session['q_index']]
    return render_template('index.html', state='question', question=next_q)

def calculate_winner():
    players = load_players()
    best_score = -1
    best_player = None

    for p in players:
        score = 0
        total_questions = len(session['answers'])
        for key, val in session['answers'].items():
            if p['stats'].get(key, 'no') == val:
                score += 1

        if score > best_score:
            best_score = score
            best_player = p

    # If match is weak (< 70%), show Mystery
    if best_score < len(session['answers']) * 0.7:
        return render_template('index.html', state='rare')

    return render_template('index.html', state='guess', player=best_player)

@app.route('/players')
def players_list():
    players_data = load_players()
    # Extract names and sort alphabetically
    names = sorted([p['name'] for p in players_data])
    return render_template('players.html', names=names)

if __name__ == '__main__':
    app.run(debug=True)