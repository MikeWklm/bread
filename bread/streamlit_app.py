"""Streamlit app for sourdough bread recipes."""
import streamlit as st

from bread import BreadRecipe

st.header('Bake a nice Sourdough Bread!')

def get_recipe(recipe_type: str) -> None:
    """Put recipe to session state from a given form.

    Args:
        recipe_type (str): absolute or relative recipe
    """
    if recipe_type == "abs":
        recipe = BreadRecipe(
            sourdough=st.session_state.abs_sourdough,
            wheat=st.session_state.abs_wheat,
            full_wheat=st.session_state.abs_full_wheat,
            water=st.session_state.abs_water,
            salt=st.session_state.abs_salt 
        )
    else:
        recipe = BreadRecipe(
        sourdough=st.session_state.rel_sourdough,
        wheat=st.session_state.rel_wheat,
        full_wheat=st.session_state.rel_full_wheat,
        water_bp=st.session_state.rel_water,
        salt_bp=st.session_state.rel_salt 
    )
    
    st.session_state.bread = recipe

if 'bread' not in st.session_state:
    st.session_state.bread = None
    
tab_rel, tab_abs = st.tabs(["Baker's Percentage", "Absolute Amounts"])

with tab_rel:
    st.text("Input your Baker's Percentage. Sourdough is assumed to have 100 % hydration.")
    with st.form("rel"):
        w_bp, s_bp = st.columns(2)
        sd, wh, fw = st.columns(3)
        sd.number_input("Sourdough [g]", min_value=25, max_value=500, value=100,
                                    help="Sourdough in grams. Assuming 100% hydration.",
                                    key="rel_sourdough")
        wh.number_input("Wheat [g]", min_value=0, max_value=2000, value=400,
                                help="Wheat in grams.", key="rel_wheat")
        fw.number_input("Full Wheat [g]", min_value=0, max_value=2000, value=100,
                                        help="Full Wheat in grams.", key="rel_full_wheat")
        w_bp.slider("Water [BP]", min_value=1.5, max_value=2., step=.01, value=1.7,
                               help="Water in Baker's Percentage.", key="rel_water")
        s_bp.slider("Salt [BP]", min_value=1., max_value=1.05, step=0.005, format="%f",
                              help="Salt in Baker's Percentage.", key="rel_salt", value=1.02)
        st.form_submit_button("Get Bread! (Rel)", on_click=get_recipe, args=["rel"])
with tab_abs:
    st.text("Input your absolute amounts. Sourdough is assumed to have 100 % hydration.")
    with st.form("abs"):
        w, s = st.columns(2)
        a_sd, a_wh, a_fw = st.columns(3)
        a_sd.number_input("Sourdough [g]", min_value=25, max_value=500, value=100,
                                    help="Sourdough in grams. Assuming 100% hydration.",
                                    key="abs_sourdough")
        a_wh.number_input("Wheat [g]", min_value=0, max_value=2000, value=400,
                                help="Wheat in grams.", key="abs_wheat")
        a_fw.number_input("Full Wheat [g]", min_value=0, max_value=2000, value=100,
                                        help="Full Wheat in grams.", key="abs_full_wheat")
        w.number_input("Water [g]", min_value=100, max_value=4000, value=350,
                               help="Water in grams.", key="abs_water")
        s.number_input("Salt [g]", min_value=1, max_value=50, value=12,
                              help="Salt in grams.", key="abs_salt")
        st.form_submit_button("Get Bread! (Abs)", on_click=get_recipe, args=["abs"])
        

if st.session_state.bread is not None:
    recipe = st.session_state.bread
    st.markdown(f"""
                ## Your Bread Recipe
                ### Total Amounts
                
                - Sourdough: __{recipe.sourdough:.0f} gramms__
                - Wheat:  __{recipe.wheat:.0f} gramms__
                - Full Wheat:  __{recipe.full_wheat:.0f} gramms__
                - Water:  __{recipe.water:.0f} gramms__
                - Salt:  __{recipe.salt:.1f} gramms__
                
                ### Relative Amounts
                
                - Salt: __{recipe.salt_bp:.3f} BP__
                - Water: __{recipe.water_bp:.2f} BP__
                - Full Wheat: __{recipe.full_wheat_percentage * 100:.1f} %__
                
                Total Bread Weight: __{recipe.total_weight:.0f} gramms__.
                """)
    
    if recipe.water_bp < 1.6:
        st.warning("Looks like your bread could need a bit more water.")
    if recipe.water_bp > 1.8:
        st.warning("If you are not expert this could become a mess. Maybe use less water?.")