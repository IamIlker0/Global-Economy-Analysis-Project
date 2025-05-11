import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
import time

ECONOMY_DATA_FILE = 'streamlit/global_economy.csv'  

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
        with open("streamlit/gdp_prediction_model.pkl", 'rb') as f:
            model_info = pickle.load(f)
            
        # Model bilgilerinin doğru yapıda olduğunu kontrol et
        if isinstance(model_info, dict) and 'model' in model_info:
            return model_info
        else:
            st.error("Model dosyası beklenen formatta değil.")
            return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model_info = load_forecast_model()
model_loaded = model_info is not None

if model_loaded:
    model = model_info['model']
    selected_features = model_info['features']
    r2_score_val = model_info.get('r2_score', 0.9887)

# Main title and description
st.markdown('<h1 class="main-header">🌍 Global Economy Analysis & Forecasting</h1>', unsafe_allow_html=True)

# Show model diagnostic information (optional - can be helpful during development)
with st.expander("Model Diagnostic Information", expanded=False):
    if model_loaded:
        st.success("Economic forecast model loaded successfully!")
        
        st.write("Model information:")
        st.write("- Model type:", type(model_info['model']))
        st.write("- Features used:", model_info['features'])
        st.write("- R² score:", model_info.get('r2_score', "Not specified"))
        
        test_data = {
            'GDP_Growth': 2.5,
            'Inflation_Rate': 3.0,
            'Unemployment_Rate': 5.0,
            'Trade_Balance': -2.5,
            'Region_Asia': 0
        }
        test_df = pd.DataFrame([test_data])
        
        st.write("Test data:", test_data)
        
        try:
            test_prediction = model_info['model'].predict(test_df)[0]
            st.write("Test forecast prediction:", test_prediction)
        except Exception as predict_error:
            st.error(f"Could not make test prediction: {predict_error}")
    else:
        st.warning("Economic forecast model not loaded. Some functionality may be limited.")

# Navigation with tabs
# tabs = st.tabs(["📊 Economic Dashboards", "📈 Economic Forecasting", "🔍 Country Comparison"])
# tab1, tab2, tab3 = tabs
tab1 = st.tabs(["📊 Economic Dashboards"])[0]

# Tab 1: Analysis Dashboards
with tab1:
    st.markdown('<div class="dashboard-main-title">Global Economy Analysis Dashboards</div>', unsafe_allow_html=True)
    loading_message = st.empty()
    
    # Dashboard selection with cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Trade Flows by Country")
        st.image("streamlit/images/changes by country.png", output_format="PNG", width=None)
        dashboard_choice1 = st.button("View Dashboard", key="db1", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Per Capita GNI Map")
        st.image("streamlit/images/Per Capita GNI, Monitoring on the World Map.png", output_format="PNG", width=None)
        dashboard_choice3 = st.button("View Dashboard", key="db3", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Sectoral Spending Distribution")
        st.image("streamlit/images/Sectoral Expenditure Analysis.png", output_format="PNG", width=None)
        dashboard_choice5 = st.button("View Dashboard", key="db5", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)   
       
        
    
    with col2:
       
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("USD Exchange Rate")
        st.image("streamlit/images/USD exchange rate according to IMF.png", output_format="PNG", width=None)
        dashboard_choice2 = st.button("View Dashboard", key="db2", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Sectors by Decades")
        st.image("streamlit/images/the values of sectors by decades.png", output_format="PNG", width=None)
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

# # Tab 2: Economic Forecasting
# with tab2:
#     st.markdown('<div class="dashboard-main-title">Economic Growth Forecasting</div>', unsafe_allow_html=True)
    
#     if model_loaded:
#         st.write("Use this tool to forecast economic growth based on various indicators.")
        
#         # Create columns for input parameters
#         col1, col2 = st.columns(2)
        
#         with col1:
#             gdp_growth = st.slider("GDP Growth Rate (%)", min_value=-5.0, max_value=10.0, value=2.5, step=0.1)
#             inflation_rate = st.slider("Inflation Rate (%)", min_value=0.0, max_value=20.0, value=3.0, step=0.1)
#             unemployment_rate = st.slider("Unemployment Rate (%)", min_value=1.0, max_value=20.0, value=5.0, step=0.1)
        
#         with col2:
#             trade_balance = st.slider("Trade Balance (% of GDP)", min_value=-15.0, max_value=15.0, value=0.0, step=0.1)
#             region_options = ["North America", "Europe", "Asia", "Latin America", "Africa", "Oceania"]
#             selected_region = st.selectbox("Region", region_options)
            
#             # Convert region to dummy variables (simplified for example)
#             region_asia = 1 if selected_region == "Asia" else 0
#             region_europe = 1 if selected_region == "Europe" else 0
#             region_north_america = 1 if selected_region == "North America" else 0
#             # Add more regions as needed
        
#         # Prepare data for prediction
#         input_data = {
#             'GDP_Growth': gdp_growth,
#             'Inflation_Rate': inflation_rate,
#             'Unemployment_Rate': unemployment_rate,
#             'Trade_Balance': trade_balance,
#             'Region_Asia': region_asia,
#             'Region_Europe': region_europe,
#             'Region_North_America': region_north_america
#             # Add more features as needed
#         }
        
#         # Create input dataframe for prediction
#         input_df = pd.DataFrame([input_data])
        
#         # Prediction button
#         if st.button("Generate Economic Forecast", use_container_width=True):
#             # Show a spinner while calculating
#             with st.spinner("Calculating forecast..."):
#                 time.sleep(1)  # Simulate computation time
                
#                 try:
#                     # Make prediction
#                     prediction = model.predict(input_df)[0]
                    
#                     # Display prediction with nice formatting
#                     st.success("Forecast Generated Successfully!")
                    
#                     # Create columns for displaying results
#                     col1, col2, col3 = st.columns(3)
                    
#                     with col1:
#                         st.metric(
#                             label="Forecasted Growth",
#                             value=f"{prediction:.2f}%",
#                             delta=f"{prediction - 2.5:.2f}%" # Comparing to global average
#                         )
                    
#                     with col2:
#                         # Create a gauge chart for the prediction
#                         fig = go.Figure(go.Indicator(
#                             mode="gauge+number",
#                             value=prediction,
#                             title={'text': "Economic Growth Potential"},
#                             gauge={
#                                 'axis': {'range': [-5, 10]},
#                                 'bar': {'color': "darkblue"},
#                                 'steps': [
#                                     {'range': [-5, 0], 'color': "red"},
#                                     {'range': [0, 3], 'color': "yellow"},
#                                     {'range': [3, 10], 'color': "green"}
#                                 ],
#                                 'threshold': {
#                                     'line': {'color': "black", 'width': 4},
#                                     'thickness': 0.75,
#                                     'value': prediction
#                                 }
#                             }
#                         ))
                        
#                         fig.update_layout(height=300)
#                         st.plotly_chart(fig, use_container_width=True)
                    
#                     with col3:
#                         # Classification based on growth rate
#                         if prediction < 0:
#                             status = "Recession"
#                             color = "🔴"
#                         elif prediction < 2:
#                             status = "Slow Growth"
#                             color = "🟠"
#                         elif prediction < 4:
#                             status = "Moderate Growth"
#                             color = "🟡"
#                         else:
#                             status = "Strong Growth"
#                             color = "🟢"
                        
#                         st.markdown(f"### Growth Status: {color} {status}")
#                         st.markdown("#### Key Factors:")
                        
#                         # List the factors that influenced the prediction
#                         factors = []
#                         if gdp_growth > 3:
#                             factors.append("Strong recent GDP growth")
#                         if inflation_rate < 2.5:
#                             factors.append("Low inflation")
#                         if unemployment_rate < 4:
#                             factors.append("Low unemployment")
#                         if trade_balance > 2:
#                             factors.append("Positive trade balance")
                        
#                         if not factors:
#                             factors = ["Balanced economic indicators"]
                        
#                         for factor in factors:
#                             st.markdown(f"- {factor}")
                
#                 except Exception as e:
#                     st.error(f"Error generating forecast: {e}")
#     else:
#         st.warning("Economic forecast model is not available. Please check the model file.")
#         st.info("You can still explore the dashboards in the first tab.")

# # Tab 3: Country Comparison
# with tab3:
#     st.markdown('<div class="dashboard-main-title">Country Economic Comparison</div>', unsafe_allow_html=True)
    
#     # Assuming we have a list of countries
#     countries = ["United States", "China", "Germany", "Japan", "United Kingdom", "France", "India", 
#                 "Brazil", "Canada", "South Korea", "Australia", "Mexico", "Indonesia", "Turkey"]
    
#     # Country selection
#     col1, col2 = st.columns(2)
    
#     with col1:
#         country1 = st.selectbox("Select Country 1", countries, index=0)
    
#     with col2:
#         # Default to second country in list
#         default_country2_index = 1 if len(countries) > 1 else 0
#         country2 = st.selectbox("Select Country 2", countries, index=default_country2_index)
    
#     # Metrics to compare
#     metrics = ["GDP Growth Rate", "Inflation Rate", "Unemployment Rate", "Trade Balance", 
#               "Public Debt", "Foreign Investment", "Currency Strength"]
    
#     selected_metrics = st.multiselect(
#         "Select Metrics to Compare",
#         metrics,
#         default=metrics[:4]  # Default to first 4 metrics
#     )
    
#     if st.button("Compare Countries", use_container_width=True):
#         if not selected_metrics:
#             st.warning("Please select at least one metric to compare.")
#         else:
#             # In a real application, you would fetch actual data here
#             # For this example, we'll use random data
            
#             # Create random comparison data for demonstration
#             np.random.seed(42)  # For reproducible results
#             comparison_data = {}
            
#             for metric in selected_metrics:
#                 if metric == "GDP Growth Rate":
#                     comparison_data[metric] = {
#                         country1: round(np.random.uniform(1.5, 4.5), 1),
#                         country2: round(np.random.uniform(1.5, 4.5), 1)
#                     }
#                 elif metric == "Inflation Rate":
#                     comparison_data[metric] = {
#                         country1: round(np.random.uniform(1.0, 6.0), 1),
#                         country2: round(np.random.uniform(1.0, 6.0), 1)
#                     }
#                 elif metric == "Unemployment Rate":
#                     comparison_data[metric] = {
#                         country1: round(np.random.uniform(3.0, 8.0), 1),
#                         country2: round(np.random.uniform(3.0, 8.0), 1)
#                     }
#                 elif metric == "Trade Balance":
#                     comparison_data[metric] = {
#                         country1: round(np.random.uniform(-5.0, 5.0), 1),
#                         country2: round(np.random.uniform(-5.0, 5.0), 1)
#                     }
#                 elif metric == "Public Debt":
#                     comparison_data[metric] = {
#                         country1: round(np.random.uniform(40.0, 120.0), 1),
#                         country2: round(np.random.uniform(40.0, 120.0), 1)
#                     }
#                 elif metric == "Foreign Investment":
#                     comparison_data[metric] = {
#                         country1: round(np.random.uniform(10.0, 50.0), 1),
#                         country2: round(np.random.uniform(10.0, 50.0), 1)
#                     }
#                 else:  # Currency Strength
#                     comparison_data[metric] = {
#                         country1: round(np.random.uniform(0.7, 1.3), 2),
#                         country2: round(np.random.uniform(0.7, 1.3), 2)
#                     }
            
#             # Display comparison
#             st.subheader(f"Economic Comparison: {country1} vs {country2}")
            
#             # Create a radar chart for comparison
#             if len(selected_metrics) >= 3:  # Need at least 3 metrics for a meaningful radar chart
#                 categories = selected_metrics
                
#                 fig = go.Figure()
                
#                 # Add traces for each country
#                 fig.add_trace(go.Scatterpolar(
#                     r=[comparison_data[metric][country1] for metric in categories],
#                     theta=categories,
#                     fill='toself',
#                     name=country1
#                 ))
                
#                 fig.add_trace(go.Scatterpolar(
#                     r=[comparison_data[metric][country2] for metric in categories],
#                     theta=categories,
#                     fill='toself',
#                     name=country2
#                 ))
                
#                 # Update layout
#                 fig.update_layout(
#                     polar=dict(
#                         radialaxis=dict(
#                             visible=True,
#                         )
#                     ),
#                     showlegend=True,
#                     height=500
#                 )
                
#                 st.plotly_chart(fig, use_container_width=True)
            
#             # Create a table comparison
#             comparison_table = []
#             for metric in selected_metrics:
#                 value1 = comparison_data[metric][country1]
#                 value2 = comparison_data[metric][country2]
                
#                 if metric in ["GDP Growth Rate", "Inflation Rate", "Unemployment Rate", "Trade Balance"]:
#                     unit = "%"
#                 elif metric == "Public Debt":
#                     unit = "% of GDP"
#                 elif metric == "Foreign Investment":
#                     unit = "Billion USD"
#                 else:  # Currency Strength
#                     unit = "Index"
                
#                 comparison_table.append({
#                     "Metric": metric,
#                     f"{country1}": f"{value1} {unit}",
#                     f"{country2}": f"{value2} {unit}",
#                     "Difference": f"{abs(value1 - value2):.1f} {unit}"
#                 })
            
#             comparison_df = pd.DataFrame(comparison_table)
#             st.table(comparison_df)
            
#             # Summary of comparison
#             st.subheader("Comparison Summary")
            
#             # Count advantages for each country
#             advantages1 = 0
#             advantages2 = 0
            
#             summary_points = []
            
#             for metric in selected_metrics:
#                 value1 = comparison_data[metric][country1]
#                 value2 = comparison_data[metric][country2]
                
#                 # For most metrics, higher is better, except inflation, unemployment, and public debt
#                 if metric in ["Inflation Rate", "Unemployment Rate", "Public Debt"]:
#                     if value1 < value2:
#                         advantages1 += 1
#                         summary_points.append(f"✅ {country1} has lower {metric.lower()} ({value1} vs {value2})")
#                     elif value2 < value1:
#                         advantages2 += 1
#                         summary_points.append(f"✅ {country2} has lower {metric.lower()} ({value2} vs {value1})")
#                 else:
#                     if value1 > value2:
#                         advantages1 += 1
#                         summary_points.append(f"✅ {country1} has higher {metric.lower()} ({value1} vs {value2})")
#                     elif value2 > value1:
#                         advantages2 += 1
#                         summary_points.append(f"✅ {country2} has higher {metric.lower()} ({value2} vs {value1})")
            
#             # Display summary points
#             for point in summary_points:
#                 st.markdown(point)
            
#             # Overall comparison result
#             if advantages1 > advantages2:
#                 st.success(f"Based on selected metrics, {country1} shows stronger economic performance.")
#             elif advantages2 > advantages1:
#                 st.success(f"Based on selected metrics, {country2} shows stronger economic performance.")
#             else:
#                 st.info(f"Based on selected metrics, {country1} and {country2} show comparable economic performance.")

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
