import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

ECONOMY_DATA_FILE = 'global_economy.csv'

# Page configuration
st.set_page_config(
    page_title="Global Economy Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .dashboard-main-title {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: white;
        background-color: #084272;
        padding: 8px 15px;
        border-radius: 5px;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #003366;
    }
    .dashboard-card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s;
        cursor: pointer;
        background-color: #1E2A38;
        color: white;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# Load the dataset
@st.cache_data
def load_economy_data():
    try:
        return pd.read_csv(ECONOMY_DATA_FILE)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

economy_data = load_economy_data()


dashboard_embed_codes = {
    "Trade Flows by Country": """
    <div style='border-radius: 10px; overflow: hidden; padding: 10px; background-color: #f0f0f0; margin: 0 auto; width: 95%; max-width: 2000px;'>
        <div style='background-color: #4b3f72; color: #ffd166; padding: 8px; margin-bottom: 10px; border-radius: 8px; text-align: center; font-weight: bold; max-width: 600px; margin-left: auto; margin-right: auto;'>
            For better viewing please use the full screen button in the bottom right corner.
        </div>
        <div class='tableauPlaceholder' id='viz1745348885230' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='changes by country ' src='https://public.tableau.com/static/images/ch/changesbycountry/changesbycountry/1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz' style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
                <param name='embed_code_version' value='3' />
                <param name='site_root' value='' />
                <param name='name' value='changesbycountry/changesbycountry' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https://public.tableau.com/static/images/ch/changesbycountry/changesbycountry/1.png' />
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>
        <script type='text/javascript'>
            var divElement = document.getElementById('viz1745348885230');
            var vizElement = divElement.getElementsByTagName('object')[0];
            if (divElement.offsetWidth > 800) {
                vizElement.style.width='100%';
                vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
            } else if (divElement.offsetWidth > 500) {
                vizElement.style.width='100%';
                vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
            } else {
                vizElement.style.width='100%';
                vizElement.style.height='777px';
            }
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        </script>
    </div>
    """,
    
    "Sectoral Spending Distribution": """
    <div style='border-radius: 10px; overflow: hidden; padding: 10px; background-color: #f0f0f0; margin: 0 auto; width: 95%; max-width: 1200px;'>
        <div style='background-color: #4b3f72; color: #ffd166; padding: 8px; margin-bottom: 10px; border-radius: 8px; text-align: center; font-weight: bold; max-width: 600px; margin-left: auto; margin-right: auto;'>
            For better viewing please use the full screen button in the bottom right corner.
        </div>
        <div class='tableauPlaceholder' id='viz1745348967203' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Sectoral Spending Distribution by Country and Year ' src='https://public.tableau.com/static/images/Se/SectoralSpendingDistributionbyCountryandYear/SectoralExpenditureAnalysis/1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz' style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
                <param name='embed_code_version' value='3' />
                <param name='site_root' value='' />
                <param name='name' value='SectoralSpendingDistributionbyCountryandYear/SectoralExpenditureAnalysis' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https://public.tableau.com/static/images/Se/SectoralSpendingDistributionbyCountryandYear/SectoralExpenditureAnalysis/1.png' />
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>
        <script type='text/javascript'>
            var divElement = document.getElementById('viz1745348967203');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width='100%';
            vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        </script>
    </div>
    """,
    
    "Per Capita GNI Map": """
    <div style='border-radius: 10px; overflow: hidden; padding: 10px; background-color: #f0f0f0; margin: 0 auto; width: 95%; max-width: 1200px;'>
        <div style='background-color: #4b3f72; color: #ffd166; padding: 8px; margin-bottom: 10px; border-radius: 8px; text-align: center; font-weight: bold; max-width: 600px; margin-left: auto; margin-right: auto;'>
            For better viewing please use the full screen button in the bottom right corner.
        </div>
        <div class='tableauPlaceholder' id='viz1745349196215' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='Per Capita GNI, Monitoring on the World Map ' src='https://public.tableau.com/static/images/Pe/PerCapitaGNIMonitoringontheWorldMap/PerCapitaGNIMonitoringontheWorldMap/1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz' style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
                <param name='embed_code_version' value='3' />
                <param name='site_root' value='' />
                <param name='name' value='PerCapitaGNIMonitoringontheWorldMap/PerCapitaGNIMonitoringontheWorldMap' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https://public.tableau.com/static/images/Pe/PerCapitaGNIMonitoringontheWorldMap/PerCapitaGNIMonitoringontheWorldMap/1.png' />
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>
        <script type='text/javascript'>
            var divElement = document.getElementById('viz1745349196215');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width='100%';
            vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        </script>
    </div>
    """,
    
    "Sectors by Decades": """
    <div style='border-radius: 10px; overflow: hidden; padding: 10px; background-color: #f0f0f0; margin: 0 auto; width: 95%; max-width: 1200px;'>
        <div style='background-color: #4b3f72; color: #ffd166; padding: 8px; margin-bottom: 10px; border-radius: 8px; text-align: center; font-weight: bold; max-width: 600px; margin-left: auto; margin-right: auto;'>
            For better viewing please use the full screen button in the bottom right corner.
        </div>
        <div class='tableauPlaceholder' id='viz1745349238940' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='The values of sectors by decades ' src='https://public.tableau.com/static/images/th/thevaluesofsectorsbydecades/thevaluesofsectorsbydecades/1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz' style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
                <param name='embed_code_version' value='3' />
                <param name='site_root' value='' />
                <param name='name' value='thevaluesofsectorsbydecades/thevaluesofsectorsbydecades' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https://public.tableau.com/static/images/th/thevaluesofsectorsbydecades/thevaluesofsectorsbydecades/1.png' />
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>
        <script type='text/javascript'>
            var divElement = document.getElementById('viz1745349238940');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width='100%';
            vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        </script>
    </div>
    """,
    
    "USD Exchange Rate": """
    <div style='border-radius: 10px; overflow: hidden; padding: 10px; background-color: #f0f0f0; margin: 0 auto; width: 95%; max-width: 1200px;'>
        <div style='background-color: #4b3f72; color: #ffd166; padding: 8px; margin-bottom: 10px; border-radius: 8px; text-align: center; font-weight: bold; max-width: 600px; margin-left: auto; margin-right: auto;'>
            For better viewing please use the full screen button in the bottom right corner.
        </div>
        <div class='tableauPlaceholder' id='viz1745349277437' style='position: relative'>
            <noscript>
                <a href='#'>
                    <img alt='According to IMF, USD exchange rate by Country ' src='https://public.tableau.com/static/images/US/USDexchangerateaccordingtoIMF/USDexchangerateaccordingtoIMF/1_rss.png' style='border: none' />
                </a>
            </noscript>
            <object class='tableauViz' style='display:none;'>
                <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />
                <param name='embed_code_version' value='3' />
                <param name='site_root' value='' />
                <param name='name' value='USDexchangerateaccordingtoIMF/USDexchangerateaccordingtoIMF' />
                <param name='tabs' value='no' />
                <param name='toolbar' value='yes' />
                <param name='static_image' value='https://public.tableau.com/static/images/US/USDexchangerateaccordingtoIMF/USDexchangerateaccordingtoIMF/1.png' />
                <param name='animate_transition' value='yes' />
                <param name='display_static_image' value='yes' />
                <param name='display_spinner' value='yes' />
                <param name='display_overlay' value='yes' />
                <param name='display_count' value='yes' />
                <param name='language' value='en-US' />
            </object>
        </div>
        <script type='text/javascript'>
            var divElement = document.getElementById('viz1745349277437');
            var vizElement = divElement.getElementsByTagName('object')[0];
            vizElement.style.width='100%';
            vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
            var scriptElement = document.createElement('script');
            scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
            vizElement.parentNode.insertBefore(scriptElement, vizElement);
        </script>
    </div>
    """
}

# Load ML model for economic forecasting
@st.cache_resource
def load_forecast_model():
    try:
        # First try to load model with metadata
        try:
            model_data = joblib.load("gdp_prediction_model_with_metadata.pkl")
            return model_data
        except:
            # Fallback: Original model + manual features
            model = joblib.load("gdp_prediction_model.pkl")
            
            # EXACT feature list from notebook (13 features)
            selected_features = [
                'AMA_exchange_rate',
                'IMF_based_exchange_rate', 
                'Population',
                'Per_capita_GNI',
                'Agriculture_hunting_forestry_fishing_ISIC_A_B',
                'Changes_in_inventories',
                'Construction_ISIC_F',
                'General_government_final_consumption_expenditure',
                'Manufacturing_ISIC_D',
                'Mining_Manufacturing_Utilities_ISIC_C_E',
                'Other_Activities_ISIC_J_P',
                'Transport_storage_and_communication_ISIC_I',
                'Wholesale_retail_trade_restaurants_and_hotels_ISIC_G_H'
            ]
            
            return {
                'model': model,
                'features': selected_features,
                'r2_score': 0.9887
            }

    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model_info = load_forecast_model()
model_loaded = model_info is not None
model_info = load_forecast_model()
model_loaded = model_info is not None

if model_loaded:
    model = model_info['model']
    selected_features = model_info['features']
    r2_score_val = model_info.get('r2_score', 0.9887)

# Main title and description
st.markdown('<h1 class="main-header">🌍 Global Economy Analysis & Forecasting</h1>', unsafe_allow_html=True)

# Show model diagnostic information
with st.expander("Model Diagnostic Information", expanded=False):
    if model_loaded:
        st.success("✅ Economic forecast model loaded successfully!")
        
        st.write("**Model Information:**")
        st.write(f"- Model type: {type(model_info['model'])}")
        st.write(f"- Features count: {len(model_info['features'])}")
        st.write(f"- R² score: {model_info.get('r2_score', 'Not specified')}")
        
        st.write("**Features used by model:**")
        for i, feature in enumerate(model_info['features'], 1):
            st.write(f"{i}. {feature}")
        
        # Test prediction to check if model works
        try:
            # Prepare test data (13 features)
            test_data = np.array([[1.0, 1.0, 50000000, 10000, 500, 0, 25, 1000, 800, 600, 400, 300, 700]])
            test_prediction = model_info['model'].predict(test_data)[0]
            st.success(f"✅ Model test successful! Sample prediction: ${test_prediction:,.2f}")
        except Exception as predict_error:
            st.error(f"❌ Model test failed: {predict_error}")
    else:
        st.warning("⚠️ Economic forecast model not loaded. Some functionality may be limited.")


# Navigation with tabs
tabs = st.tabs(["📊 Economic Dashboards", "📈 Economic Forecasting", "🔍 Country Comparison"])
tab1, tab2, tab3 = tabs
# tab1 = st.tabs(["📊 Economic Dashboards"])[0]

# Tab 1: Analysis Dashboards
with tab1:
    st.markdown('<div class="dashboard-main-title">Global Economy Analysis Dashboards</div>', unsafe_allow_html=True)
    loading_message = st.empty()
    
    # Dashboard selection with cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Trade Flows by Country")
        st.image("images/changes by country.png", output_format="PNG", width=None)
        dashboard_choice1 = st.button("View Dashboard", key="db1", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Per Capita GNI Map")
        st.image("images/Per Capita GNI, Monitoring on the World Map.png", output_format="PNG", width=None)
        dashboard_choice3 = st.button("View Dashboard", key="db3", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Sectoral Spending Distribution")
        st.image("images/Sectoral Expenditure Analysis.png", output_format="PNG", width=None)
        dashboard_choice5 = st.button("View Dashboard", key="db5", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)   
       
        
    
    with col2:
       
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("USD Exchange Rate")
        st.image("images/USD exchange rate according to IMF.png", output_format="PNG", width=None)
        dashboard_choice2 = st.button("View Dashboard", key="db2", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Sectors by Decades")
        st.image("images/the values of sectors by decades.png", output_format="PNG", width=None)
        dashboard_choice4 = st.button("View Dashboard", key="db4", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dashboard display section
    dashboard_displayed = False
    
    if dashboard_choice1 or dashboard_choice2 or dashboard_choice3 or dashboard_choice4 or dashboard_choice5:
        loading_message.success("Dashboard is loading. You can view it by scrolling down.")
        dashboard_displayed = True
        st.markdown('<div id="dashboard-view" class="dashboard-view"></div>', unsafe_allow_html=True)
        st.info("💡 **Please make it full screen for better viewing.**")
        
        if dashboard_choice1:
            st.markdown("### Trade Flows by Country Dashboard")
            components.html(dashboard_embed_codes["Trade Flows by Country"], height=800, scrolling=True)
        elif dashboard_choice2:
            st.markdown("### USD Exchange Rate Dashboard")
            components.html(dashboard_embed_codes["USD Exchange Rate"], height=800, scrolling=True)
        elif dashboard_choice3:
            st.markdown("### Per Capita GNI Map Dashboard")
            components.html(dashboard_embed_codes["Per Capita GNI Map"], height=800, scrolling=True)
        elif dashboard_choice4:
            st.markdown("### Sectors by Decades Dashboard")
            components.html(dashboard_embed_codes["Sectors by Decades"], height=800, scrolling=True)
        elif dashboard_choice5:
            st.markdown("### Sectoral Spending Distribution Dashboard")
            components.html(dashboard_embed_codes["Sectoral Spending Distribution"], height=800, scrolling=True)
            
    
    if not dashboard_displayed:
        st.info("👆 Select a dashboard above or explore the other tabs to use our forecasting tools.")

# Tab 2: FIX - Economic Forecasting
with tab2:
    st.markdown('<div class="dashboard-main-title">Economic Forecasting</div>', unsafe_allow_html=True)
    
    if not model_loaded:
        st.error("Model could not be loaded. Prediction unavailable.")
    else:
        st.write("""
        **Advanced GDP Prediction Model** - Uses the Random Forest model trained in the notebook.
        """)
        
        st.info(f"Model uses {len(model_info['features'])} economic indicators and has {model_info['r2_score']*100:.2f}% accuracy.")
        
        # User input section - ALL 13 features
        st.subheader("Enter Economic Indicators")
        
        # User-friendly names for features
        feature_display = {
            'AMA_exchange_rate': {'name': 'AMA Exchange Rate', 'default': 1.0, 'help': 'Local currency / USD'},
            'IMF_based_exchange_rate': {'name': 'IMF Exchange Rate', 'default': 1.0, 'help': 'IMF official exchange rate'},
            'Population': {'name': 'Population', 'default': 50000000, 'help': 'Total population count'},
            'Per_capita_GNI': {'name': 'Per Capita GNI (USD)', 'default': 10000, 'help': 'Gross National Income per person'},
            'Agriculture_hunting_forestry_fishing_ISIC_A_B': {'name': 'Agriculture Value (Million USD)', 'default': 500.0, 'help': 'Agriculture sector value added'},
            'Changes_in_inventories': {'name': 'Changes in Inventories (Million USD)', 'default': 0.0, 'help': 'Inventory changes'},
            'Construction_ISIC_F': {'name': 'Construction Value (Million USD)', 'default': 25.0, 'help': 'Construction sector value'},
            'General_government_final_consumption_expenditure': {'name': 'Government Expenditure (Million USD)', 'default': 1000.0, 'help': 'Government final consumption expenditure'},
            'Manufacturing_ISIC_D': {'name': 'Manufacturing Value (Million USD)', 'default': 800.0, 'help': 'Manufacturing sector value'},
            'Mining_Manufacturing_Utilities_ISIC_C_E': {'name': 'Mining & Utilities (Million USD)', 'default': 600.0, 'help': 'Mining and utilities value'},
            'Other_Activities_ISIC_J_P': {'name': 'Other Activities (Million USD)', 'default': 400.0, 'help': 'Other economic activities'},
            'Transport_storage_and_communication_ISIC_I': {'name': 'Transport & Communication (Million USD)', 'default': 300.0, 'help': 'Transport sector value'},
            'Wholesale_retail_trade_restaurants_and_hotels_ISIC_G_H': {'name': 'Trade & Hotels (Million USD)', 'default': 700.0, 'help': 'Wholesale/retail trade and hospitality'}
        }
        
        # Two-column layout
        col1, col2 = st.columns(2)
        
        inputs = {}
        for i, feature in enumerate(model_info['features']):
            display_info = feature_display[feature]
            
            # Alternate columns
            column = col1 if i % 2 == 0 else col2
            
            with column:
                inputs[feature] = st.number_input(
                    display_info['name'],
                    value=float(display_info['default']),
                    format="%.2f",
                    help=display_info['help'],
                    key=f"input_{feature}"
                )
        
        # Prediction button
        if st.button("🔮 Make GDP Prediction", type="primary"):
            try:
                # Prepare input array - EXACT feature order
                input_array = np.array([[inputs[feature] for feature in model_info['features']]])
                
                st.write("**Debug Information:**")
                st.write(f"Input shape: {input_array.shape}")
                st.write(f"Expected features: {len(model_info['features'])}")
                
                # Make prediction
                prediction = model_info['model'].predict(input_array)[0]
                
                # Show result
                st.success(f"## 💰 Predicted GDP: ${prediction:,.2f} USD")
                
                # Show input values
                with st.expander("Review Input Values"):
                    for feature, value in inputs.items():
                        friendly_name = feature_display[feature]['name']
                        st.write(f"• {friendly_name}: {value:,.2f}")
                
                # Reference GDP values
                with st.expander("Reference GDP Values (2022)"):
                    gdp_examples = {
                        "United States": "25.46 trillion USD",
                        "China": "17.96 trillion USD", 
                        "Japan": "4.41 trillion USD",
                        "Germany": "4.07 trillion USD",
                        "India": "3.39 trillion USD",
                        "Turkey": "819.0 billion USD"
                    }
                    
                    for country, gdp in gdp_examples.items():
                        st.write(f"- {country}: {gdp}")
                
            except Exception as e:
                st.error(f"❌ Prediction error: {e}")
                st.write("**Possible causes:**")
                st.write("- Input data format error")
                st.write("- Model file corrupted")
                
        # Sample test button
        if st.button("🧪 Test with Sample Data"):
            try:
                # Test with known values
                sample_values = [1.0, 1.0, 50000000, 10000, 500, 0, 25, 1000, 800, 600, 400, 300, 700]
                sample_array = np.array([sample_values])
                sample_prediction = model_info['model'].predict(sample_array)[0]
                
                st.success(f"Sample prediction: ${sample_prediction:,.2f}")
                st.info("✅ Model is working correctly!")
            except Exception as e:
                st.error(f"❌ Test failed: {e}")

with tab3:
    st.markdown('<div class="dashboard-main-title">Country Economic Comparison</div>', unsafe_allow_html=True)
    
    # Get countries from CSV
    countries = sorted(economy_data['Country'].unique().tolist())
    
    # Country selection
    col1, col2 = st.columns(2)
    
    with col1:
        country1 = st.selectbox("Select Country 1", countries, index=0)
    
    with col2:
        # Default to second country in list
        default_country2_index = 1 if len(countries) > 1 else 0
        country2 = st.selectbox("Select Country 2", countries, index=default_country2_index)
    
   # Economic metrics from CSV (use correct column names)
    metrics = [
        "Per_capita_GNI",
        "Gross_Domestic_Product_GDP",
        "Gross_National_IncomeGNI_in_USD",
        "Gross_capital_formation",
        "Exports_of_goods_and_services",
        "Imports_of_goods_and_services"
    ]

    # Metric labels and units
    metric_info = {
        # Underscore versions (original column names)
        "Per_capita_GNI": {"label": "Per Capita GNI", "unit": "USD"},
        "Gross_Domestic_Product_GDP": {"label": "GDP", "unit": "Million USD"},
        "Gross_National_IncomeGNI_in_USD": {"label": "GNI", "unit": "Million USD"},
        "Gross_capital_formation": {"label": "Capital Formation", "unit": "Million USD"},
        "Exports_of_goods_and_services": {"label": "Exports", "unit": "Million USD"},
        "Imports_of_goods_and_services": {"label": "Imports", "unit": "Million USD"},
        
        # Space versions (displayed labels)
        "Per Capita GNI": {"label": "Per Capita GNI", "unit": "USD"},
        "GDP": {"label": "GDP", "unit": "Million USD"},
        "GNI": {"label": "GNI", "unit": "Million USD"},
        "Capital Formation": {"label": "Capital Formation", "unit": "Million USD"},
        "Exports": {"label": "Exports", "unit": "Million USD"},
        "Imports": {"label": "Imports", "unit": "Million USD"}
    }
    
    # Metric selection
    selected_metrics = st.multiselect(
        "Select Economic Indicators to Compare",
        metrics,
        default=metrics[:4],
        format_func=lambda x: metric_info[x]["label"]
    )
    
    # Year selection
    available_years = sorted(economy_data['Year'].unique(), reverse=True)
    selected_year = st.selectbox("Select Year for Comparison", available_years, index=0)
    

    if st.button("Compare Countries", use_container_width=True):
        if not selected_metrics:
            st.warning("Please select at least one economic indicator to compare.")
        else:
            # Fetch real data from CSV
            comparison_data = {}
            
            for metric in selected_metrics:
                # Find value for Country1
                country1_data = economy_data[(economy_data['Country'] == country1) & 
                                        (economy_data['Year'] == selected_year)]
                
                # Find value for Country2
                country2_data = economy_data[(economy_data['Country'] == country2) & 
                                        (economy_data['Year'] == selected_year)]
                
                if not country1_data.empty and metric in country1_data.columns and not country2_data.empty and metric in country2_data.columns:
                    val1 = country1_data[metric].values[0]
                    val2 = country2_data[metric].values[0]
                    
                    # Replace NaN values with 0
                    val1 = 0 if pd.isna(val1) else val1
                    val2 = 0 if pd.isna(val2) else val2
                    
                    comparison_data[metric] = {
                        country1: val1,
                        country2: val2
                    }
                else:
                    # If data is missing, assign default value
                    comparison_data[metric] = {
                        country1: 0,
                        country2: 0
                    }
            
            # Display comparison
            st.subheader(f"Economic Comparison ({selected_year}): {country1} vs {country2}")
            
            # Radar chart for comparison
            if comparison_data and len(selected_metrics) >= 3:
                # Prepare data for radar chart
                categories = []
                values1 = []
                values2 = []
                
                for metric in selected_metrics:
                    if metric in comparison_data:
                        # Use user-friendly labels
                        friendly_name = metric_info[metric]["label"] if metric in metric_info else metric
                        categories.append(friendly_name)
                        
                        # Get values and normalize
                        val1 = comparison_data[metric][country1]
                        val2 = comparison_data[metric][country2]
                        
                        # Skip if both values are 0
                        if val1 == 0 and val2 == 0:
                            continue
                        
                        # Normalize large values
                        max_val = max(val1, val2) if max(val1, val2) > 0 else 1
                        norm_val1 = (val1 / max_val) * 100
                        norm_val2 = (val2 / max_val) * 100
                        
                        values1.append(norm_val1)
                        values2.append(norm_val2)
                
                # Radar chart
                fig = go.Figure()
                
                # Add trace for first country
                fig.add_trace(go.Scatterpolar(
                    r=values1,
                    theta=categories,
                    fill='toself',
                    name=country1,
                    line_color='royalblue'
                ))
                
                # Add trace for second country
                fig.add_trace(go.Scatterpolar(
                    r=values2,
                    theta=categories,
                    fill='toself',
                    name=country2,
                    line_color='crimson'
                ))
                
                # Configure chart appearance
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    title=f"Economic Indicators Comparison ({selected_year})",
                    showlegend=True,
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add detailed explanation below the chart
                st.info("""
                **How to Interpret This Radar Chart:**

                This radar chart shows relative values (normalized to 100%) to enable easier comparison between economies of different sizes. For each indicator:

                - The country with the higher value receives 100% on that axis
                - The other country's value is shown as a percentage relative to the higher value
                - A larger overall area indicates better economic performance on the selected metrics

                **Note:** This normalization method allows comparison of economies of vastly different sizes, but means that the leading country will always show 100% on each metric where it leads. The actual values can be seen in the table below.
                """)            
            # Bar chart for comparison (if fewer than 3 metrics or radar chart not shown)
            elif comparison_data:
                chart_data = []
                
                for metric in selected_metrics:
                    if metric in comparison_data:
                        chart_data.append({
                            "Metric": metric_info[metric]["label"],
                            country1: comparison_data[metric][country1],
                            country2: comparison_data[metric][country2]
                        })
                
                chart_df = pd.DataFrame(chart_data)
                
                # Plotly bar chart - normalize values for better comparison
                fig = go.Figure()
                
                for metric in chart_df["Metric"]:
                    row = chart_df[chart_df["Metric"] == metric]
                    val1 = row[country1].values[0]
                    val2 = row[country2].values[0]
                    
                    # Skip if both values are 0
                    if val1 == 0 and val2 == 0:
                        continue
                    
                    # Normalize values for comparison
                    max_val = max(val1, val2) if max(val1, val2) > 0 else 1
                    norm_val1 = (val1 / max_val) * 100
                    norm_val2 = (val2 / max_val) * 100
                    
                    fig.add_trace(go.Bar(
                        x=[metric],
                        y=[norm_val1],
                        name=f"{country1}",
                        marker_color='royalblue',
                        text=f"{val1:,.0f} {metric_info[metric]['unit']}",
                        textposition='auto',
                        offsetgroup=0
                    ))
                    
                    fig.add_trace(go.Bar(
                        x=[metric],
                        y=[norm_val2],
                        name=f"{country2}",
                        marker_color='crimson',
                        text=f"{val2:,.0f} {metric_info[metric]['unit']}",
                        textposition='auto',
                        offsetgroup=1
                    ))
                
                fig.update_layout(
                    title=f"Economic Indicators Comparison ({selected_year})",
                    barmode='group',
                    height=500,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    yaxis=dict(title="Relative Value (%)")
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Create a table comparison
            comparison_table = []
            for metric in selected_metrics:
                if metric in comparison_data:
                    value1 = comparison_data[metric][country1]
                    value2 = comparison_data[metric][country2]
                    unit = metric_info[metric]["unit"]
                    
                    # Calculate difference and percentage difference
                    diff = value1 - value2
                    if value2 != 0:
                        pct_diff = (diff / abs(value2)) * 100
                    else:
                        pct_diff = 0 if value1 == 0 else 100
                    
                    comparison_table.append({
                        "Indicator": metric_info[metric]["label"],
                        f"{country1}": f"{value1:,.0f} {unit}",
                        f"{country2}": f"{value2:,.0f} {unit}",
                        "Difference": f"{diff:,.0f} {unit} ({pct_diff:.1f}%)"
                    })
            
            comparison_df = pd.DataFrame(comparison_table)
            st.table(comparison_df)
            
            # Summary of comparison
            st.subheader("Economic Overview")
            
            # Count advantages for each country
            advantages1 = 0
            advantages2 = 0
            
            summary_points = []
            
            for metric in selected_metrics:
                if metric in comparison_data:
                    value1 = comparison_data[metric][country1]
                    value2 = comparison_data[metric][country2]
                    label = metric_info[metric]["label"]
                    unit = metric_info[metric]["unit"]
                    
                    # For all these metrics, higher is generally better
                    if value1 > value2 and value1 > 0:
                        advantages1 += 1
                        pct_higher = ((value1 - value2) / value2) * 100 if value2 > 0 else 100
                        summary_points.append(f"✅ {country1} has higher {label} ({value1:,.0f} vs {value2:,.0f} {unit}, {pct_higher:.1f}% higher)")
                    elif value2 > value1 and value2 > 0:
                        advantages2 += 1
                        pct_higher = ((value2 - value1) / value1) * 100 if value1 > 0 else 100
                        summary_points.append(f"✅ {country2} has higher {label} ({value2:,.0f} vs {value1:,.0f} {unit}, {pct_higher:.1f}% higher)")
            
        # Display summary points
        for point in summary_points:
            st.markdown(point)
        
        # Overall comparison result
        if advantages1 > advantages2:
            st.success(f"Based on selected indicators, {country1} shows stronger economic performance in {advantages1} out of {len(selected_metrics)} areas.")
        elif advantages2 > advantages1:
            st.success(f"Based on selected indicators, {country2} shows stronger economic performance in {advantages2} out of {len(selected_metrics)} areas.")
        else:
            st.info(f"Based on selected indicators, {country1} and {country2} show comparable economic performance.")
            
    with st.expander("🔍 Advanced: View Raw Data for Selected Countries"):
        if selected_year and country1 and country2:
            year_data = economy_data[economy_data['Year'] == selected_year]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Data for {country1} in {selected_year}")
                st.dataframe(year_data[year_data['Country'] == country1])
            
            with col2:
                st.write(f"Data for {country2} in {selected_year}")
                st.dataframe(year_data[year_data['Country'] == country2])
            
            st.info("This shows all available data columns for the selected countries in the chosen year. Useful for detailed analysis beyond the selected metrics.")

# Sidebar
st.sidebar.title("About This Project")
st.sidebar.info("""
This application provides global economic analysis and forecasting using data visualization and machine learning.

**Features:**
- 4 interactive dashboards
- AI-powered economic forecasting
- Country comparison tools
- Economic trend visualization

**Model Information:**
- Algorithm: Random Forest Regression
- Training data: World Bank and IMF datasets
- Accuracy (R²): 0.92
""")

st.sidebar.title("Creator")
st.sidebar.markdown("Developer: Ilker Aydin Yilmaz")
st.sidebar.markdown("[GitHub Repository](https://github.com/IamIlker0/global-economy-analysis)")