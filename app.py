import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from math import radians, cos, sin, asin, sqrt
import random

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Northline Systems & Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# THEME COLORS
# ============================================================
BG          = "#0B1220"
CARD        = "#111827"
PRIMARY     = "#16A34A"
ACCENT      = "#FACC15"
TEXT        = "#F8FAFC"
MUTED       = "#94A3B8"
DANGER      = "#EF4444"
BORDER      = "#1E293B"

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(f"""
<style>
    .stApp {{ background-color: {BG}; }}
    [data-testid="stSidebar"] {{ background-color: {CARD}; border-right: 1px solid {BORDER}; }}
    [data-testid="stSidebar"] * {{ color: {TEXT}; }}
    .main-header {{
        background: linear-gradient(135deg, {CARD} 0%, {BG} 100%);
        padding: 1.6rem 2rem; border-radius: 14px; margin-bottom: 1.5rem;
        border-left: 6px solid {PRIMARY}; box-shadow: 0 4px 20px rgba(22, 163, 74, 0.15);
    }}
    .main-header h1 {{ color: {ACCENT}; margin: 0; font-size: 2rem; font-weight: 800; }}
    .main-header p {{ color: {MUTED}; margin: 0.4rem 0 0 0; font-size: 1rem; }}
    .insight-box {{
        background: {CARD}; border-left: 5px solid {ACCENT};
        padding: 1rem 1.3rem; border-radius: 10px; margin: 1rem 0;
        color: {TEXT}; box-shadow: 0 2px 12px rgba(250, 204, 21, 0.1);
    }}
    .insight-box b {{ color: {ACCENT}; }}
    [data-testid="stMetric"] {{
        background: {CARD}; padding: 1rem; border-radius: 10px;
        border-left: 4px solid {PRIMARY}; box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}
    [data-testid="stMetricValue"] {{ color: {TEXT}; font-weight: 800; }}
    [data-testid="stMetricLabel"] {{ color: {MUTED}; text-transform: uppercase; font-size: 0.75rem; }}
    h1, h2, h3, h4, h5 {{ color: {TEXT} !important; }}
    h3 {{ border-bottom: 2px solid {PRIMARY}; padding-bottom: 0.4rem; }}
    .stCaption, caption {{ color: {MUTED} !important; }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA: MASTER FIXTURE LIST (WEEK 1-5)
# ============================================================
FIXTURES = [
    (1, "Vision FC", 3, 0, "Young Apostles FC"), (1, "Accra Hearts of Oak SC", 4, 0, "Berekum Chelsea FC"),
    (1, "Heart of Lions FC", 0, 0, "Aduana FC"), (1, "FC Samartex 1996", 3, 1, "Karela United FC"),
    (1, "Bechem United FC", 1, 0, "Bibiani Gold Stars FC"), (1, "Basake Holy Stars FC", 1, 0, "Swedru All Blacks FC"),
    (1, "Debibi United FC", 2, 2, "Asante Kotoko SC"), (1, "Port City FC", 1, 1, "FC AshantiGold 04"),
    (1, "Dreams FC", 2, 2, "Medeama SC"),
    (2, "FC AshantiGold 04", 3, 1, "Vision FC"), (2, "Aduana FC", 0, 1, "FC Samartex 1996"),
    (2, "Swedru All Blacks FC", 1, 0, "Debibi United FC"), (2, "Young Apostles FC", 1, 0, "Basake Holy Stars FC"),
    (2, "Berekum Chelsea FC", 3, 1, "Dreams FC"), (2, "Bibiani Gold Stars FC", 1, 2, "Accra Hearts of Oak SC"),
    (2, "Asante Kotoko SC", 2, 1, "Heart of Lions FC"), (2, "Karela United FC", 3, 1, "Bechem United FC"),
    (2, "Medeama SC", 1, 0, "Port City FC"),
    (3, "Heart of Lions FC", 0, 0, "Swedru All Blacks FC"), (3, "Vision FC", 1, 1, "Medeama SC"),
    (3, "Accra Hearts of Oak SC", 0, 0, "Bechem United FC"), (3, "Port City FC", 2, 1, "Berekum Chelsea FC"),
    (3, "Aduana FC", 2, 1, "Karela United FC"), (3, "Debibi United FC", 3, 0, "Young Apostles FC"),
    (3, "Dreams FC", 2, 3, "Bibiani Gold Stars FC"), (3, "Basake Holy Stars FC", 1, 0, "FC AshantiGold 04"),
    (3, "FC Samartex 1996", 1, 1, "Asante Kotoko SC"),
    (4, "Karela United FC", 1, 0, "Accra Hearts of Oak SC"), (4, "Asante Kotoko SC", 0, 2, "Aduana FC"),
    (4, "FC AshantiGold 04", 2, 1, "Debibi United FC"), (4, "Medeama SC", 4, 1, "Basake Holy Stars FC"),
    (4, "Young Apostles FC", 1, 2, "Heart of Lions FC"), (4, "Bechem United FC", 1, 0, "Dreams FC"),
    (4, "Bibiani Gold Stars FC", 0, 2, "Port City FC"), (4, "Swedru All Blacks FC", 1, 1, "FC Samartex 1996"),
    (4, "Berekum Chelsea FC", 1, 1, "Vision FC"),
    (5, "Asante Kotoko SC", 1, 0, "Karela United FC"), (5, "Dreams FC", 0, 0, "Accra Hearts of Oak SC"),
    (5, "Vision FC", 0, 0, "Bibiani Gold Stars FC"), (5, "Aduana FC", 2, 1, "Swedru All Blacks FC"),
    (5, "Debibi United FC", 0, 1, "Medeama SC"), (5, "Port City FC", 3, 1, "Bechem United FC"),
    (5, "Heart of Lions FC", 3, 2, "FC AshantiGold 04"), (5, "Basake Holy Stars FC", 1, 0, "Berekum Chelsea FC"),
    (5, "FC Samartex 1996", 1, 0, "Young Apostles FC"),
]
df_fixtures = pd.DataFrame(FIXTURES, columns=['Week', 'Home', 'HG', 'AG', 'Away'])
df_fixtures['Score'] = df_fixtures['HG'].astype(str) + ' - ' + df_fixtures['AG'].astype(str)

COORDS = {
    'Accra Hearts of Oak SC': (5.6037, -0.1870), 'Dreams FC': (5.6037, -0.1870),
    'Vision FC': (5.6698, -0.0166), 'Young Apostles FC': (7.5833, -2.1000),
    'Berekum Chelsea FC': (7.4500, -2.5833), 'Heart of Lions FC': (6.9833, 0.2833),
    'Aduana FC': (7.2833, -2.8833), 'FC Samartex 1996': (6.0333, -2.8833),
    'Karela United FC': (9.4008, -0.8393), 'Bechem United FC': (7.0833, -2.0333),
    'Bibiani Gold Stars FC': (6.4667, -2.3333), 'Basake Holy Stars FC': (5.8167, -2.8000),
    'Swedru All Blacks FC': (5.5333, -0.7000), 'Debibi United FC': (7.7333, -2.3167),
    'Asante Kotoko SC': (6.6885, -1.6244), 'Port City FC': (6.1986, -0.3686),
    'FC AshantiGold 04': (6.2000, -1.6667), 'Medeama SC': (5.3000, -1.9833),
}

# ============================================================
# HELPERS
# ============================================================
def safe_applymap(styler, func, subset=None):
    try:
        return styler.map(func, subset=subset) if subset else styler.map(func)
    except AttributeError:
        return styler.applymap(func, subset=subset) if subset else styler.applymap(func)

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    a = sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2
    return 2 * asin(sqrt(a)) * 6371

def style_plotly(fig, height=400, legend_h=True):
    fig.update_layout(
        height=height, paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=TEXT, family="Arial"),
        legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT)) if legend_h else dict(font=dict(color=TEXT)),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, color=TEXT),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, color=TEXT),
    )
    return fig

def compute_league_table(df):
    teams = sorted(set(df['Home']) | set(df['Away']))
    rows = []
    for t in teams:
        home = df[df['Home'] == t]; away = df[df['Away'] == t]
        P = len(home) + len(away)
        W = len(home[home['HG'] > home['AG']]) + len(away[away['AG'] > away['HG']])
        D = len(home[home['HG'] == home['AG']]) + len(away[away['AG'] == away['HG']])
        L = P - W - D
        GF = int(home['HG'].sum() + away['AG'].sum())
        GA = int(home['AG'].sum() + away['HG'].sum())
        GD = GF - GA; PTS = W * 3 + D
        team_matches = pd.concat([
            df[df['Home'] == t].assign(Result=lambda x: np.where(x['HG'] > x['AG'], 'W', np.where(x['HG'] == x['AG'], 'D', 'L'))),
            df[df['Away'] == t].assign(Result=lambda x: np.where(x['AG'] > x['HG'], 'W', np.where(x['AG'] == x['HG'], 'D', 'L')))
        ]).sort_values('Week').tail(5)
        form = ' '.join(team_matches['Result'].tolist())
        rows.append({'Team': t, 'P': P, 'W': W, 'D': D, 'L': L, 'GF': GF, 'GA': GA, 'GD': GD, 'PTS': PTS, 'Form': form})
    tbl = pd.DataFrame(rows).sort_values(by=['PTS', 'GD', 'GF'], ascending=False).reset_index(drop=True)
    tbl['Pos'] = tbl.index + 1
    return tbl[['Pos', 'Team', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'PTS', 'Form']]

def compute_travel(df):
    rows = []
    for _, r in df.iterrows():
        if r['Home'] in COORDS and r['Away'] in COORDS:
            h = COORDS[r['Home']]; a = COORDS[r['Away']]
            km = haversine(a[0], a[1], h[0], h[1]) * 2
            rows.append({'Week': r['Week'], 'Team': r['Away'], 'Distance (km)': km})
    return pd.DataFrame(rows).groupby('Team')['Distance (km)'].sum().reset_index().sort_values('Distance (km)', ascending=False).reset_index(drop=True)

def team_season_stats(team, df):
    home = df[df['Home'] == team]; away = df[df['Away'] == team]
    matches = len(home) + len(away)
    wins = len(home[home['HG'] > home['AG']]) + len(away[away['AG'] > away['HG']])
    draws = len(home[home['HG'] == home['AG']]) + len(away[away['AG'] == away['HG']])
    losses = matches - wins - draws
    gf = int(home['HG'].sum() + away['AG'].sum())
    ga = int(home['AG'].sum() + away['HG'].sum())
    return {
        'Played': matches, 'Wins': wins, 'Draws': draws, 'Losses': losses,
        'GF': gf, 'GA': ga, 'GD': gf - ga, 'Points': wins*3 + draws,
        'Home GF': int(home['HG'].sum()), 'Home GA': int(home['AG'].sum()),
        'Away GF': int(away['AG'].sum()), 'Away GA': int(away['HG'].sum()),
        'Clean Sheets': len(home[home['AG'] == 0]) + len(away[away['HG'] == 0]),
        'Failed to Score': len(home[home['HG'] == 0]) + len(away[away['AG'] == 0]),
        'PPG': round((wins*3 + draws) / matches, 2) if matches > 0 else 0
    }

# ============================================================
# ML MODEL
# ============================================================
def train_poisson_model(df):
    total_home = df['HG'].sum(); total_away = df['AG'].sum()
    home_avg = max(total_home / len(df), 0.1); away_avg = max(total_away / len(df), 0.1)
    league_avg = (total_home + total_away) / (len(df) * 2)
    teams = sorted(set(df['Home']) | set(df['Away']))
    prior = 4; attack, defense = {}, {}
    for t in teams:
        h = df[df['Home'] == t]; a = df[df['Away'] == t]
        games = len(h) + len(a)
        gf = h['HG'].sum() + a['AG'].sum(); ga = h['AG'].sum() + a['HG'].sum()
        attack[t] = max((gf + prior * league_avg) / (games + prior) / league_avg, 0.25)
        defense[t] = max((ga + prior * league_avg) / (games + prior) / league_avg, 0.25)
    return attack, defense, home_avg, away_avg

def generate_remaining_fixtures(teams, played_df):
    remaining = []
    pairs = [(t1, t2) for i, t1 in enumerate(teams) for t2 in teams[i+1:]]
    for t1, t2 in pairs:
        matches = played_df[((played_df['Home'] == t1) & (played_df['Away'] == t2)) |
                            ((played_df['Home'] == t2) & (played_df['Away'] == t1))]
        for _ in range(2 - len(matches)):
            remaining.append((t1, t2) if random.random() < 0.5 else (t2, t1))
    return remaining

def simulate_season(attack, defense, home_avg, away_avg, current_table, n_sims=2000):
    teams = current_table['Team'].tolist()
    base_pts = dict(zip(current_table['Team'], current_table['PTS']))
    base_gd = dict(zip(current_table['Team'], current_table['GD']))
    base_gf = dict(zip(current_table['Team'], current_table['GF']))
    random.seed(42)
    remaining = generate_remaining_fixtures(teams, df_fixtures)
    finish_positions = {t: [] for t in teams}; final_pts_dist = {t: [] for t in teams}
    for _ in range(n_sims):
        pts = base_pts.copy(); gd = base_gd.copy(); gf = base_gf.copy()
        for home, away in remaining:
            xg_h = attack[home] * defense[away] * home_avg
            xg_a = attack[away] * defense[home] * away_avg
            hg = np.random.poisson(max(xg_h, 0.05)); ag = np.random.poisson(max(xg_a, 0.05))
            gf[home] += hg; gf[away] += ag; gd[home] += hg - ag; gd[away] += ag - hg
            if hg > ag: pts[home] += 3
            elif ag > hg: pts[away] += 3
            else: pts[home] += 1; pts[away] += 1
        standings = sorted(teams, key=lambda t: (pts[t], gd[t], gf[t]), reverse=True)
        for pos, t in enumerate(standings, 1): finish_positions[t].append(pos)
        for t in teams: final_pts_dist[t].append(pts[t])
    summary = []
    for t in teams:
        pos = finish_positions[t]
        summary.append({'Team': t, 'Current Pts': base_pts[t], 'Projected Pts': round(np.mean(final_pts_dist[t]), 1),
                        'Title %': round(sum(1 for p in pos if p == 1) / n_sims * 100, 1),
                        'Top 4 %': round(sum(1 for p in pos if p <= 4) / n_sims * 100, 1),
                        'Relegation %': round(sum(1 for p in pos if p >= 17) / n_sims * 100, 1),
                        'Avg Finish': round(np.mean(pos), 1)})
    return pd.DataFrame(summary).sort_values('Avg Finish').reset_index(drop=True)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown(f"""
<div style="text-align:center; padding: 1rem 0;">
    <div style="font-size: 2.5rem;">⚽</div>
    <div style="font-size: 1.1rem; font-weight: 800; color: {ACCENT};">NORTHLINE</div>
    <div style="font-size: 0.7rem; color: {MUTED}; letter-spacing: 2px;">SYSTEMS & ANALYTICS</div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

PAGE = st.sidebar.radio("📂 Navigate", [
    "🏠 Dashboard", "📊 League Table", "⚽ Results", "📈 Stats (WK1-5)",
    "🚌 Travel Analysis", "📉 Form Guide", "🛡️ Weakest Defense",
    "🔍 Team Analysis", "📅 Fixtures", "🤖 ML Projections", "⚔️ Match Predictor"
])
st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='color:{MUTED}; font-size: 0.8rem;'>📅 Updated through Matchweek 5</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='color:{MUTED}; font-size: 0.8rem;'>🐍 Built with Python + Streamlit</div>", unsafe_allow_html=True)

table = compute_league_table(df_fixtures)

# ============================================================
# PAGE: DASHBOARD
# ============================================================
if PAGE == "🏠 Dashboard":
    st.markdown(f'<div class="main-header"><h1>GPL 2026/27 ANALYTICS</h1><p>Official Season Hub — Updated through Matchweek 5</p></div>', unsafe_allow_html=True)

    total_goals = int(df_fixtures['HG'].sum() + df_fixtures['AG'].sum())
    total_games = len(df_fixtures)

    top_attack_team = table.loc[table['GF'].idxmax()]
    best_defense_team = table.loc[table['GA'].idxmin()]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏆 Leader", table.iloc[0]['Team'], f"{table.iloc[0]['PTS']} pts")
    c2.metric("⚽ Total Goals", total_goals, f"{total_goals/total_games:.2f}/game")
    c3.metric("📅 Games Played", total_games, "MW 1-5")
    c4.metric("🔥 Top Attack", top_attack_team['Team'], f"{int(top_attack_team['GF'])} goals")

    st.markdown("---")
    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("🏆 Current Top 5 Standings")
        top5 = table.head(5)
        fig = go.Figure(go.Bar(
            x=top5['PTS'], y=top5['Team'], orientation='h',
            marker=dict(color=[PRIMARY, ACCENT, "#22C55E", "#EAB308", "#4ADE80"], line=dict(color=BG, width=1)),
            text=top5['PTS'], textposition='outside', textfont=dict(size=20, color=TEXT, family='Arial Black')
        ))
        fig = style_plotly(fig, height=380, legend_h=False)
        fig.update_layout(yaxis=dict(autorange='reversed', tickfont=dict(size=14, color=TEXT)), xaxis_title="Points")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("📊 Season Snapshot")
        c = st.columns(2)
        c[0].metric("Home Wins", len(df_fixtures[df_fixtures['HG'] > df_fixtures['AG']]))
        c[1].metric("Away Wins", len(df_fixtures[df_fixtures['AG'] > df_fixtures['HG']]))
        c = st.columns(2)
        c[0].metric("Draws", len(df_fixtures[df_fixtures['HG'] == df_fixtures['AG']]))
        c[1].metric("Goals/Game", f"{total_goals/total_games:.2f}")

    st.markdown("---")
    st.markdown("### 💡 Key Insights")
    st.markdown(f"""
    <div class="insight-box">
    <b>🏆 Title Race:</b> {table.iloc[0]['Team']} leads with {table.iloc[0]['PTS']} points.<br><br>
    <b>🔥 Top Attack:</b> {top_attack_team['Team']} with {int(top_attack_team['GF'])} goals scored.<br><br>
    <b>🛡️ Best Defense:</b> {best_defense_team['Team']} (only {int(best_defense_team['GA'])} conceded).<br><br>
    <b>🚌 Travel Kings:</b> Karela United — most traveled team in the league.<br><br>
    <b>📉 Strugglers:</b> Dreams FC sit bottom with {table.iloc[-1]['PTS']} points.
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PAGE: LEAGUE TABLE
# ============================================================
elif PAGE == "📊 League Table":
    st.markdown(f'<div class="main-header"><h1>OFFICIAL LEAGUE TABLE</h1><p>After Matchweek 5 — Only the Top 1 team qualifies for continental competition</p></div>', unsafe_allow_html=True)

    def color_row(row):
        if row['Pos'] == 1: return [f'background-color: rgba(22, 163, 74, 0.25); color: {TEXT}'] * len(row)
        if row['Pos'] >= 17: return [f'background-color: rgba(239, 68, 68, 0.25); color: {TEXT}'] * len(row)
        return [f'color: {TEXT}'] * len(row)

    def color_form(val):
        if 'W' in str(val): return f'color: {PRIMARY}; font-weight: bold'
        return f'color: {MUTED}'

    styled = table.style.apply(color_row, axis=1).set_properties(**{'color': TEXT, 'background-color': BG})
    styled = safe_applymap(styled, color_form, subset=['Form'])
    st.dataframe(styled, use_container_width=True, hide_index=True, height=700)
    st.caption("🟢 Top 1 (Continental slot)  |  🔴 Bottom 2 (Relegation zone)")

# ============================================================
# PAGE: RESULTS
# ============================================================
elif PAGE == "⚽ Results":
    st.markdown(f'<div class="main-header"><h1>MATCH RESULTS</h1><p>All 45 games from Matchweek 1 to 5</p></div>', unsafe_allow_html=True)
    week_filter = st.selectbox("Filter by Matchweek", ["All Matchweeks"] + [f"Matchweek {i}" for i in range(1, 6)])
    df_show = df_fixtures.copy()
    if week_filter != "All Matchweeks":
        wk = int(week_filter.split()[-1]); df_show = df_show[df_show['Week'] == wk]
    for wk in sorted(df_show['Week'].unique()):
        wk_df = df_show[df_show['Week'] == wk]
        goals = int(wk_df['HG'].sum() + wk_df['AG'].sum())
        st.markdown(f"#### 📅 Matchweek {wk} — {len(wk_df)} matches, {goals} goals")
        display_df = wk_df[['Home', 'Score', 'Away']].rename(columns={'Home': '🏠 Home', 'Score': 'Score', 'Away': 'Away ✈️'})
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=min(400, 50 + len(wk_df) * 40))

# ============================================================
# PAGE: STATS
# ============================================================
elif PAGE == "📈 Stats (WK1-5)":
    st.markdown(f'<div class="main-header"><h1>HEAD-TO-HEAD STATS</h1><p>Matchweek 1 vs 2 vs 3 vs 4 vs 5</p></div>', unsafe_allow_html=True)
    stats = []
    for wk in range(1, 6):
        wk_df = df_fixtures[df_fixtures['Week'] == wk]
        stats.append({'Week': f'WK {wk}', 'Games': len(wk_df), 'Total Goals': int(wk_df['HG'].sum() + wk_df['AG'].sum()),
                      'Home Goals': int(wk_df['HG'].sum()), 'Away Goals': int(wk_df['AG'].sum()),
                      'Home Wins': len(wk_df[wk_df['HG'] > wk_df['AG']]), 'Away Wins': len(wk_df[wk_df['AG'] > wk_df['HG']]),
                      'Draws': len(wk_df[wk_df['HG'] == wk_df['AG']])})
    df_stats = pd.DataFrame(stats).set_index('Week').T
    st.markdown("### 📊 Weekly Breakdown")
    st.dataframe(df_stats.style.set_properties(**{'text-align': 'center', 'font-size': '15px', 'font-weight': 'bold', 'color': TEXT, 'background-color': CARD}), use_container_width=True, height=340)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📈 Goals Trend")
        plot_df = df_stats.loc[['Total Goals', 'Home Goals', 'Away Goals']].T.reset_index()
        plot_df.columns = ['Week', 'Total Goals', 'Home Goals', 'Away Goals']
        fig = px.line(plot_df, x='Week', y=['Total Goals', 'Home Goals', 'Away Goals'], markers=True,
                      color_discrete_sequence=[PRIMARY, ACCENT, "#22C55E"],
                      labels={'value': 'Goals', 'variable': 'Type'})
        fig.update_traces(line=dict(width=4), marker=dict(size=12, line=dict(color=BG, width=2)))
        fig = style_plotly(fig, height=400)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### 🎯 Outcome Distribution")
        outcome_df = df_stats.loc[['Home Wins', 'Away Wins', 'Draws']].T.reset_index()
        outcome_df.columns = ['Week', 'Home Wins', 'Away Wins', 'Draws']
        fig = px.bar(outcome_df, x='Week', y=['Home Wins', 'Away Wins', 'Draws'], barmode='group',
                     color_discrete_sequence=[PRIMARY, ACCENT, MUTED],
                     labels={'value': 'Matches', 'variable': 'Outcome'})
        fig = style_plotly(fig, height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE: TRAVEL
# ============================================================
elif PAGE == "🚌 Travel Analysis":
    st.markdown(f'<div class="main-header"><h1>TRAVEL ANALYSIS</h1><p>Total round-trip kilometers from Matchweek 1 to 5</p></div>', unsafe_allow_html=True)
    travel = compute_travel(df_fixtures)
    st.markdown("### 🚌 Does Travel Fatigue Affect Team Performance?")
    colors = [PRIMARY if i == 0 else ACCENT if i == 1 else "#22C55E" if i == 2 else MUTED for i in range(len(travel))]
    fig = go.Figure(go.Bar(x=travel['Distance (km)'], y=travel['Team'], orientation='h',
                           marker=dict(color=colors, line=dict(color=BG, width=1)),
                           text=travel['Distance (km)'].round(0).astype(int).astype(str) + ' km',
                           textposition='outside', textfont=dict(size=14, color=TEXT, family='Arial Black')))
    fig = style_plotly(fig, height=750, legend_h=False)
    fig.update_layout(yaxis=dict(autorange='reversed', tickfont=dict(size=14, color=TEXT)),
                      xaxis_title="Total Round-Trip Distance (km)", margin=dict(l=10, r=160, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"""<div class="insight-box"><b>💡 Key Insight:</b> <b>{travel.iloc[0]['Team']}</b> has traveled <b>{int(travel.iloc[0]['Distance (km)']):,} km</b>!<br>
    <b>🎯 Most Rested:</b> {travel.iloc[-1]['Team']} — only {int(travel.iloc[-1]['Distance (km)']):,} km.</div>""", unsafe_allow_html=True)

# ============================================================
# PAGE: FORM GUIDE
# ============================================================
elif PAGE == "📉 Form Guide":
    st.markdown(f'<div class="main-header"><h1>FORM GUIDE</h1><p>Last 5 results for every team</p></div>', unsafe_allow_html=True)
    form_table = table[['Pos', 'Team', 'Form', 'PTS', 'GD']].copy()
    def color_form_cell(val):
        val = str(val)
        if val == 'W': return f'background-color: {PRIMARY}; color: white; font-weight: bold; text-align: center'
        if val == 'D': return f'background-color: {ACCENT}; color: {BG}; font-weight: bold; text-align: center'
        if val == 'L': return f'background-color: {DANGER}; color: white; font-weight: bold; text-align: center'
        return f'color: {TEXT}'
    styled = safe_applymap(form_table.style, color_form_cell, subset=['Form'])
    styled = styled.set_properties(**{'color': TEXT, 'background-color': CARD})
    st.dataframe(styled, use_container_width=True, hide_index=True, height=700)

# ============================================================
# PAGE: WEAKEST DEFENSE
# ============================================================
elif PAGE == "🛡️ Weakest Defense":
    st.markdown(f'<div class="main-header"><h1>🛡️ DEFENSIVE ANALYSIS</h1><p>Who is leaking the most goals in the GPL?</p></div>', unsafe_allow_html=True)

    defense_df = table[['Pos', 'Team', 'P', 'GA', 'GD', 'PTS']].copy()
    defense_df = defense_df.sort_values('GA', ascending=False).reset_index(drop=True)
    defense_df['GA/Game'] = (defense_df['GA'] / defense_df['P']).round(2)

    st.markdown("### 🚨 Top 5 Leakiest Defenses")
    worst5 = defense_df.head(5)
    colors = [DANGER, "#F97316", ACCENT, "#EAB308", MUTED]
    fig = go.Figure(go.Bar(
        x=worst5['GA'], y=worst5['Team'], orientation='h',
        marker=dict(color=colors, line=dict(color=BG, width=1)),
        text=worst5['GA'].astype(str) + ' goals', textposition='outside',
        textfont=dict(size=16, color=TEXT, family='Arial Black')
    ))
    fig = style_plotly(fig, height=380, legend_h=False)
    fig.update_layout(yaxis=dict(autorange='reversed', tickfont=dict(size=14, color=TEXT)),
                      xaxis_title="Goals Conceded")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ✅ Top 5 Best Defenses")
    best5 = defense_df.sort_values('GA').head(5)
    colors_best = [PRIMARY, "#22C55E", "#4ADE80", "#86EFAC", MUTED]
    fig = go.Figure(go.Bar(
        x=best5['GA'], y=best5['Team'], orientation='h',
        marker=dict(color=colors_best, line=dict(color=BG, width=1)),
        text=best5['GA'].astype(str) + ' goals', textposition='outside',
        textfont=dict(size=16, color=TEXT, family='Arial Black')
    ))
    fig = style_plotly(fig, height=380, legend_h=False)
    fig.update_layout(yaxis=dict(autorange='reversed', tickfont=dict(size=14, color=TEXT)),
                      xaxis_title="Goals Conceded")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📋 Full Defensive Ranking")
    st.dataframe(defense_df[['Team', 'P', 'GA', 'GA/Game', 'GD', 'PTS']].style.set_properties(
        **{'color': TEXT, 'background-color': CARD}), use_container_width=True, hide_index=True)

# ============================================================
# PAGE: TEAM ANALYSIS
# ============================================================
elif PAGE == "🔍 Team Analysis":
    st.markdown(f'<div class="main-header"><h1>🔍 INDIVIDUAL TEAM ANALYSIS</h1><p>Deep dive into every team\'s season performance</p></div>', unsafe_allow_html=True)

    teams = sorted(COORDS.keys())
    selected_team = st.selectbox("🎯 Select a Team", teams)

    stats = team_season_stats(selected_team, df_fixtures)
    pos = table[table['Team'] == selected_team]['Pos'].values[0]

    st.markdown(f"## {selected_team}  <span style='color:{ACCENT};'>#{int(pos)}</span>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Points", stats['Points'], f"{stats['PPG']} PPG")
    c2.metric("Played", stats['Played'])
    c3.metric("Record", f"{stats['Wins']}W-{stats['Draws']}D-{stats['Losses']}L")
    c4.metric("Goals", f"{stats['GF']}-{stats['GA']}", f"GD {stats['GD']:+d}")
    c5.metric("Clean Sheets", stats['Clean Sheets'])

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏠 Home vs Away (Goals)")
        home_away_df = pd.DataFrame({
            'Location': ['Home', 'Away'],
            'Goals For': [stats['Home GF'], stats['Away GF']],
            'Goals Against': [stats['Home GA'], stats['Away GA']]
        })
        fig = px.bar(home_away_df, x='Location', y=['Goals For', 'Goals Against'], barmode='group',
                     color_discrete_sequence=[PRIMARY, DANGER],
                     labels={'value': 'Goals', 'variable': ''})
        fig = style_plotly(fig, height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📊 Attack vs Defense Radar")
        max_gf = table['GF'].max() or 1
        max_ga = table['GA'].max() or 1
        attack_score = (stats['GF'] / max_gf) * 100
        defense_score = (1 - (stats['GA'] / max_ga)) * 100
        ppg_score = min((stats['PPG'] / 3) * 100, 100)
        clean_score = min((stats['Clean Sheets'] / 5) * 100, 100)
        consistency = 100 - (stats['Losses'] / stats['Played']) * 100 if stats['Played'] > 0 else 0

        radar_df = pd.DataFrame({
            'Metric': ['Attack', 'Defense', 'Points/Game', 'Clean Sheets', 'Consistency'],
            'Score': [attack_score, defense_score, ppg_score, clean_score, consistency]
        })
        fig = go.Figure(go.Scatterpolar(
            r=radar_df['Score'].tolist() + [radar_df['Score'].iloc[0]],
            theta=radar_df['Metric'].tolist() + [radar_df['Metric'].iloc[0]],
            fill='toself', line=dict(color=PRIMARY, width=3),
            fillcolor='rgba(22, 163, 74, 0.3)'
        ))
        fig.update_layout(
            polar=dict(
                bgcolor=BG,
                radialaxis=dict(visible=True, range=[0, 100], gridcolor=BORDER, tickfont=dict(color=MUTED)),
                angularaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT, size=12))
            ),
            showlegend=False, height=350, paper_bgcolor=BG, font=dict(color=TEXT),
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚽ Match Log")
    team_matches = pd.concat([
        df_fixtures[df_fixtures['Home'] == selected_team].assign(
            Location='🏠 Home', Opponent=lambda x: x['Away'],
            Team_Score=lambda x: x['HG'], Opp_Score=lambda x: x['AG']),
        df_fixtures[df_fixtures['Away'] == selected_team].assign(
            Location='✈️ Away', Opponent=lambda x: x['Home'],
            Team_Score=lambda x: x['AG'], Opp_Score=lambda x: x['HG'])
    ]).sort_values('Week')
    team_matches['Result'] = team_matches.apply(
        lambda r: '🟢 W' if r['Team_Score'] > r['Opp_Score'] else ('🟡 D' if r['Team_Score'] == r['Opp_Score'] else '🔴 L'), axis=1)
    team_matches['Score'] = team_matches['Team_Score'].astype(str) + ' - ' + team_matches['Opp_Score'].astype(str)

    display = team_matches[['Week', 'Location', 'Opponent', 'Score', 'Result']].rename(columns={'Week': 'MW'})
    st.dataframe(display, use_container_width=True, hide_index=True)

# ============================================================
# PAGE: FIXTURES
# ============================================================
elif PAGE == "📅 Fixtures":
    st.markdown(f'<div class="main-header"><h1>SEASON FIXTURES</h1><p>All matches played so far</p></div>', unsafe_allow_html=True)
    df_show = df_fixtures[['Week', 'Home', 'Score', 'Away']].rename(columns={'Week': 'MW', 'Home': '🏠 Home', 'Away': 'Away ✈️'})
    st.dataframe(df_show, use_container_width=True, hide_index=True, height=750)

# ============================================================
# PAGE: ML PROJECTIONS
# ============================================================
elif PAGE == "🤖 ML Projections":
    st.markdown(f'<div class="main-header"><h1>ML SEASON PROJECTIONS</h1><p>Poisson-based Monte Carlo simulation (2,000 seasons)</p></div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="insight-box"><b>🔮 How It Works:</b> Poisson regression + Bayesian shrinkage → 2,000 alternate futures.</div>""", unsafe_allow_html=True)
    with st.spinner("⏳ Running 2,000 season simulations..."):
        attack, defense, home_avg, away_avg = train_poisson_model(df_fixtures)
        proj = simulate_season(attack, defense, home_avg, away_avg, table, n_sims=2000)
    st.markdown("### 🏆 Projected Final Standings")
    display_cols = ['Team', 'Current Pts', 'Projected Pts', 'Title %', 'Top 4 %', 'Relegation %', 'Avg Finish']
    styled = (proj[display_cols].style.background_gradient(subset=['Title %'], cmap='Greens')
              .background_gradient(subset=['Relegation %'], cmap='Reds')
              .set_properties(**{'color': TEXT, 'background-color': CARD})
              .format({'Projected Pts': '{:.1f}', 'Title %': '{:.1f}%', 'Top 4 %': '{:.1f}%',
                       'Relegation %': '{:.1f}%', 'Avg Finish': '{:.1f}'}))
    st.dataframe(styled, use_container_width=True, hide_index=True, height=680)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏆 Title Race Probability")
        title_df = proj.nlargest(6, 'Title %')[['Team', 'Title %']]
        fig = px.bar(title_df, x='Title %', y='Team', orientation='h', color_discrete_sequence=[PRIMARY], text='Title %')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color=TEXT, size=13, family='Arial Black'))
        fig = style_plotly(fig, height=350, legend_h=False)
        fig.update_layout(yaxis=dict(autorange='reversed'), xaxis_title="Chance of winning the title (%)")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("### 📉 Relegation Risk")
        rel_df = proj.nlargest(6, 'Relegation %')[['Team', 'Relegation %']]
        fig = px.bar(rel_df, x='Relegation %', y='Team', orientation='h', color_discrete_sequence=[DANGER], text='Relegation %')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside', textfont=dict(color=TEXT, size=13, family='Arial Black'))
        fig = style_plotly(fig, height=350, legend_h=False)
        fig.update_layout(yaxis=dict(autorange='reversed'), xaxis_title="Chance of relegation (%)")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# PAGE: MATCH PREDICTOR
# ============================================================
elif PAGE == "⚔️ Match Predictor":
    st.markdown(f'<div class="main-header"><h1>MATCH PREDICTOR</h1><p>Choose two teams to see the AI-predicted outcome</p></div>', unsafe_allow_html=True)
    attack, defense, home_avg, away_avg = train_poisson_model(df_fixtures)
    teams = sorted(COORDS.keys())
    col1, col2 = st.columns(2)
    with col1: home_team = st.selectbox("🏠 Home Team", teams, index=teams.index("Medeama SC"))
    with col2: away_team = st.selectbox("✈️ Away Team", teams, index=teams.index("Accra Hearts of Oak SC"))
    if home_team == away_team:
        st.warning("⚠️ Please pick two different teams.")
    else:
        xg_h = attack[home_team] * defense[away_team] * home_avg
        xg_a = attack[away_team] * defense[home_team] * away_avg
        np.random.seed(42); sims = 10000
        h_goals = np.random.poisson(xg_h, sims); a_goals = np.random.poisson(xg_a, sims)
        home_win = (h_goals > a_goals).mean() * 100; draw = (h_goals == a_goals).mean() * 100; away_win = (h_goals < a_goals).mean() * 100
        scorelines = {}
        for h, a in zip(h_goals, a_goals): scorelines[(h, a)] = scorelines.get((h, a), 0) + 1
        top_scores = sorted(scorelines.items(), key=lambda x: x[1], reverse=True)[:5]
        st.markdown(f"## {home_team} 🆚 {away_team}")
        c1, c2, c3 = st.columns(3)
        c1.metric(f"🏠 {home_team} Win", f"{home_win:.1f}%"); c2.metric("⚖️ Draw", f"{draw:.1f}%"); c3.metric(f"✈️ {away_team} Win", f"{away_win:.1f}%")
        st.markdown(f"**Expected Goals:** {home_team} **{xg_h:.2f}** — **{xg_a:.2f}** {away_team}")
        fig = go.Figure(data=[go.Pie(labels=[f'{home_team} Win', 'Draw', f'{away_team} Win'], values=[home_win, draw, away_win],
                                     hole=0.55, marker=dict(colors=[PRIMARY, ACCENT, DANGER], line=dict(color=BG, width=3)),
                                     textinfo='label+percent', textfont=dict(color=TEXT, size=13, family='Arial Black'))])
        fig.update_layout(paper_bgcolor=BG, plot_bgcolor=BG, font=dict(color=TEXT), height=420, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("### 🎯 Most Likely Scorelines")
        score_df = pd.DataFrame([{'Score': f"{h} - {a}", 'Probability': f"{v/sims*100:.1f}%"} for (h, a), v in top_scores])
        st.dataframe(score_df, use_container_width=True, hide_index=True)