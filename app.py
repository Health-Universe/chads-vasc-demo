import os
current_path = os.path.abspath(__file__).rsplit("/", 1)[0]
csv_path = f"{current_path}/data.csv"
import pandas as pd

from model import chads_vasc_score, template


### Streamlit ###
import streamlit as st

# Text
st.markdown("## [CHA₂DS₂-VASc Score](https://www.mdcalc.com/calc/801/cha2ds2-vasc-score-atrial-fibrillation-stroke-risk#pearls-pitfalls) for Atrial Fibrillation Stroke Risk")
st.divider()

# Columns
col1, col2 = st.columns(2)

# Inputs
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

age = col1.number_input("Age", min_value=0, max_value=120, value=65)

sex = col2.radio("Sex", ["Male", "Female"])

chf = col1.checkbox("Congestive Heart Failure (CHF)")
hypertension = col2.checkbox("Hypertension")
stroke_tia = col1.checkbox("Stroke or Transient Ischemic Attack (TIA)")
vascular_disease = col2.checkbox("Vascular Disease")
diabetes = col1.checkbox("Diabetes")

# Output
score = chads_vasc_score(age=age, 
                female={"Male": False, "Female": True}[sex], 
                chf=chf, 
                hypertension=hypertension,
                stroke_tia=stroke_tia, 
                vascular_disease=vascular_disease, 
                diabetes=diabetes)

col2.info(f"CHA₂DS₂-VASc Score: {score}")

st.divider()
col3, col4 = st.columns(2)

# Plotting
df = pd.read_csv(csv_path)
col3.dataframe(df)
col4.line_chart(data=df, x="CHA2DS2-VASc Score", 
                y=["Risk of ischemic stroke", "Risk of stroke/TIA/systemic embolism"])

st.markdown("Friberg L, Rosenqvist M, Lip GY. Evaluation of risk stratification schemes for ischaemic stroke and bleeding in 182 678 patients with atrial fibrillation: the Swedish Atrial Fibrillation cohort study. Eur Heart J. 2012 Jun;33(12):1500-10. doi: 10.1093/eurheartj/ehr488. Epub 2012 Jan 13. PMID: 22246443.")


### LangChain ###
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import create_csv_agent

if len(openai_api_key) > 0:

    st.divider()
    col5, col6 = st.columns(2)

    # LLM
    model_name = st.sidebar.radio("Model", ["gpt-4", "gpt-3.5-turbo"], horizontal=True)
    st.sidebar.markdown("Note. GPT-4 is recommended for better performance.")

    os.environ["OPENAI_API_KEY"] = openai_api_key
    llm = ChatOpenAI(model_name=model_name, temperature=0.0)
    
    # Prompt/Chain
    col5.markdown("#### Is Anticoagulation Indicated?")
    if col5.button("Run", key="prompt_chain_button"):
        with st.spinner("Running"):

            prompt = PromptTemplate(
                input_variables=["score", "sex"],
                template=template,
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            output = chain.run({"score": score, "sex": sex})

            col5.info(output)


    # Tool(kits)/Agent
    col6.markdown("#### What Is The Stroke Risk?")

    stroke_type = col6.radio("Stroke Type", ["Ischemic", "Embolic"], horizontal=True)

    if col6.button("Run", key="toolkit_agent_button"):
        with st.spinner("Running"):

            agent = create_csv_agent(llm, csv_path, verbose=True)
            output = agent.run(f"What is the risk of {stroke_type} stroke for a score of {score}")

            col6.info(f"{stroke_type} Risk: {output}")

st.divider()
with st.expander("Disclaimer"):
    st.markdown("""Please read the following disclaimer carefully before using this medical application (the "App").

This App is intended for informational and educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. The information, content, and tools provided in this App are not intended to replace or modify any information, services, or treatment provided by a qualified healthcare professional.

The developers and creators of this App make no representation, warranty, or guarantee, either expressed or implied, regarding the accuracy, completeness, or appropriateness of the information, content, or tools found within this App. Furthermore, we expressly disclaim any liability, loss, or risk incurred as a direct or indirect consequence of the use, application, or interpretation of any information provided in the App.

You, the user, are solely responsible for determining the value and appropriateness of any information or material available through this App. It is crucial to always seek the advice of a physician, medical professional, or other qualified healthcare providers with any questions, concerns or symptoms you may have regarding your health or any medical condition. Never disregard, avoid, or delay seeking appropriate medical attention because of something you have read or learned through this App.

If you believe you have a medical emergency, call your healthcare provider or emergency services immediately. This App should not be relied upon in urgent or emergency situations. It is essential to rely on the advice of qualified healthcare professionals to assess and address your specific health needs.

By using this App, you hereby agree to indemnify and hold the developers, creators, and any affiliated parties harmless from any liability, loss, claim, or expense (including reasonable attorney's fees) arising out of or related to your use of this App or its contents.

This App may contain links to third-party websites or services. We do not control, endorse, or assume any responsibility for the content, privacy policy, or practices of such websites or services. You acknowledge and agree that this App's developers and creators shall not be responsible or liable, directly or indirectly, for any damage or loss caused by, or in connection with, the use of or reliance on any site or service.

The developers and creators of this App reserve the right to modify or discontinue the App, or any features therein, at any time, without notice.

By using this App, you agree to be bound by this Disclaimer. If you do not agree with any part of this Disclaimer, please refrain from using the App.
    
    """)
