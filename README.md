# CHA₂DS₂-VASc Score Demo

This is a demo for deploying a [FastAPI](https://fastapi.tiangolo.com) app and [Streamlit](https://streamlit.io) app with LangChain to [Health Universe](https://www.healthuniverse.com/).

## Essential Links

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Streamlit Docs](https://docs.streamlit.io)
- [LangChain Docs](https://python.langchain.com/en/latest/index.html)

### Further Reading
- [OpenAI Cookbook](https://github.com/openai/openai-cookbook#prompting-guide)
- [GPT Best Practice](https://platform.openai.com/docs/guides/gpt-best-practices)

## Getting Started

There are five files in this project:

- `model.py`: Script for calculating CHA₂DS₂-VASc score based on [MDCalc](https://www.mdcalc.com/calc/801/cha2ds2-vasc-score-atrial-fibrillation-stroke-risk).
- `main.py`: Script for running FastAPI app.
- `app.py`: Script for running Streamlit app.
- `data.csv`: Table from [MDCalc](https://www.mdcalc.com/calc/801/cha2ds2-vasc-score-atrial-fibrillation-stroke-risk) of stroke risk based on CHA₂DS₂-VASc score.
- `requirements.txt`: Project dependencies.

Below are the essential FastAPI, Streamlit, and LangChain code in this project.

### 1. FastAPI: `main.py`

```python
# Import FastAPI
from fastapi import FastAPI
```

```python
# Instantiate App
app = FastAPI()
```

```python
# Decorate Function
@app.get("/")
def run(age: int = 65, female: bool = True, ...) -> int:
    score =  chads_vasc_score(age=age, 
                    female=female, 
                    chf=chf, 
                    hypertension=hypertension,
                    stroke_tia=stroke_tia, 
                    vascular_disease=vascular_disease, 
                    diabetes=diabetes)
    return f"CHA₂DS₂-VASc Score: {score}"
```

To learn more about parameters and FastAPI see:
- [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)

### 2. Streamlit: `app.py`

#### 2.1. Text

```python
## Markdown (markdown gives more flexibility than "header" or "wrote")
st.markdown("## [CHA₂DS₂-VASc Score](https://www.mdcalc.com/ ...
```

```python
## Divider (add between sections)
st.divider()
```

#### 2.2. Columns

```python
# Columns (if no columns use "st.")
col1, col2 = st.columns(2)
```

#### 2.3. Inputs

```python
## Text input (not sidebar)
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
```

```python
## Number input (can set default values)
age = col1.number_input("Age", min_value=0, max_value=120, value=65)
```

```python
## Radio input (returns list value)
sex = col2.radio("Sex", ["Male", "Female"])
```

```python
## Checkbox inputs (returns bool)
chf = col1.checkbox("Congestive Heart Failure (CHF)")
...
```

#### 2.4. Outputs

```python
score = chads_vasc_score(age=age, ...

## Info output (other options "success", "warning", "error")
col2.info(f"CHA₂DS₂-VASc Score: {score}")
```

#### 2.5. Plotting

```python
## Dataframe
col3.dataframe(df)
```

```python
## Chart
col4.line_chart(data=df, x="CHA2DS2-VASc Score", ...
```

#### 2.6. Other

```python
## Button
if col5.button("Run", key="prompt_chain_button"):
```

```python
## Spinner
with st.spinner("Running"):
```

### 3. LangChain: `app.py`

#### 3.1. Large Language Models (LLMs)

```python
## Set OpenAI API Key (get from https://platform.openai.com/account/api-keys)
os.environ["OPENAI_API_KEY"] = openai_api_key
```

```python
## Instantiate model
llm = ChatOpenAI(model_name=model_name, temperature=0.0)
```

#### 3.2. Prompts and Chains

```python
## Create template
template = """
        Task: Determine if anticoagulation is recommended ...
```
```python       
## Create prompt based on template
prompt = PromptTemplate(
    input_variables=["score", "sex"],
    template=template,
)
```

```python
## Load LLM and prompt to chain
chain = LLMChain(llm=llm, prompt=prompt)
```

```python
## Run chain
output = chain.run({"score": score, "sex": sex})
```

#### 3.3. Tools and Agents

```python
## Create agent (this comes preloaded with CSV toolkit)
agent = create_csv_agent(llm, csv_path, verbose=True)
```

```python
## Run agent
output = agent.run(f"What is the risk of {stroke_type} stroke for a score of {score}")
```

For ways to create custom tools for agents see:

- [Defining Custom Tools](https://python.langchain.com/en/latest/modules/agents/tools/custom_tools.html)
- [Multi-Input Tools](https://python.langchain.com/en/latest/modules/agents/tools/multi_input_tool.html)