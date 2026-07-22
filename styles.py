CUSTOM_CSS = """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #F0EEE9 0%, #C5D3CE 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #E1DDD3 0%, #A4BBB4 100%);
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input,
    div[data-baseweb="select"] > div {
        background-color: #F6F5F2 !important;
        color: #1A1A1A !important;
        border: 1px solid #D5DAD8 !important;
        border-radius: 6px !important;
    }
    div[data-testid="stSelectbox"] span, 
    div[data-baseweb="select"] aria-live {
        color: #1A1A1A !important;
    }
    div[data-testid="stMetric"] {
        background-color: #F6F5F2 !important;
        border: 1px solid #D5DAD8 !important;
        border-radius: 12px;
        padding: 12px;
    }
    div[data-testid="stDataFrame"] {
        background-color: #F6F5F2 !important;
        border: 1px solid #D5DAD8 !important;
        border-radius: 12px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #E2E1DC !important;
        border-radius: 8px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #1A1A1A !important;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #F6F5F2 !important;
        border-radius: 6px;
    }
    p, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown {
        color: #1A1A1A !important;
    }
    </style>
    """