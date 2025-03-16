import streamlit as st
import pint
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.let_it_rain import rain
from streamlit_extras.toggle_switch import st_toggle_switch

def convert_units(value, from_unit, to_unit):
    ureg = pint.UnitRegistry()
    currency_rates = {
        "USD": {"PKR": 278, "EUR": 0.91, "GBP": 0.78, "INR": 83.5},
        "PKR": {"USD": 0.0036, "EUR": 0.0033, "GBP": 0.0028, "INR": 0.30},
        "EUR": {"USD": 1.10, "PKR": 303, "GBP": 0.86, "INR": 91.5},
        "GBP": {"USD": 1.28, "PKR": 352, "EUR": 1.16, "INR": 106.7},
        "INR": {"USD": 0.012, "PKR": 3.35, "EUR": 0.011, "GBP": 0.0094}
    }
    
    try:
        if from_unit in currency_rates and to_unit in currency_rates[from_unit]:
            return round(value * currency_rates[from_unit][to_unit], 2)
        elif from_unit in ["celsius", "fahrenheit", "kelvin"] and to_unit in ["celsius", "fahrenheit", "kelvin"]:
            temp = ureg.Quantity(value, ureg(from_unit))
            return temp.to(to_unit).magnitude
        else:
            result = (value * ureg(from_unit)).to(to_unit)
            return result.magnitude
    except Exception as e:
        return f"Oops! Something went wrong: {e}"

def main():
    st.set_page_config(page_title="🌍 Friendly Unit Converter", page_icon="🔄", layout="centered")
    colored_header("🔄 Convert Anything, Anytime!", "A simple and friendly way to convert units", color_name="blue-70")
    
    st.markdown(
        """
        <style>
            .stButton>button {
                background-color: #28a745;
                color: white;
                border-radius: 10px;
                font-size: 18px;
                padding: 10px;
            }
            .stSelectbox, .stNumberInput {
                border-radius: 10px;
            }
        </style>
        """, unsafe_allow_html=True
    )
    
    dark_mode = st_toggle_switch("🌙 Dark Mode", default_value=False)
    if dark_mode:
        st.markdown("""
            <style>
                body { background-color: #121212; color: white; }
                .stSelectbox, .stNumberInput { background-color: #333; color: white; }
            </style>
        """, unsafe_allow_html=True)
    
    st.write("👋 Hey there! Need to convert something? Just enter your value, pick your units, and let me handle the rest!")
    
    categories = {
        "📏 Length": ["meter", "kilometer", "mile", "yard", "foot", "inch"],
        "⚖️ Weight": ["gram", "kilogram", "pound", "ounce"],
        "🌡️ Temperature": ["celsius", "fahrenheit", "kelvin"],
        "⏳ Time": ["second", "minute", "hour", "day"],
        "🧴 Volume": ["liter", "milliliter", "gallon", "cubic meter"],
        "💱 Currency": ["USD", "EUR", "GBP", "PKR", "INR"],
    }
    
    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("📌 Choose a category", list(categories.keys()))
    with col2:
        value = st.number_input("✏️ Enter your value", min_value=0.0, step=0.1, format="%.2f")
    
    col3, col4 = st.columns(2)
    with col3:
        from_unit = st.selectbox("🎯 Convert from", categories[category])
    with col4:
        to_unit = st.selectbox("📍 Convert to", categories[category])
    
    if st.button("✨ Show me the magic!"):
        result = convert_units(value, from_unit, to_unit)
        st.success(f"🎉 {value} {from_unit} is equal to {result} {to_unit}!")
    
    st.markdown("💡 *Tip: Try converting miles to kilometers, or Celsius to Fahrenheit!* 🧠")
    style_metric_cards()
    rain(emoji="🌟", font_size=20, falling_speed=5, animation_length="infinite")
    
if __name__ == "__main__":
    main()
