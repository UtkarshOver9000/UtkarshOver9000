# Hi, I'm Utkarsh (Xen)

I build machine-learning and security projects and test them on **real public data**.
Every number below comes from a held-out evaluation and is documented, with its data
source, in the project's README.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/utkarsh-sharma-15845a319)
[![Email](https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white)](mailto:utkarshs123op@gmail.com)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?logo=instagram&logoColor=white)](https://instagram.com/utkarsh.over9000)

## Projects

### Security

**[Aegis: login risk scoring](https://github.com/UtkarshOver9000/Aegis-Auth-Anomaly-Engine)** · [live demo](https://impossible-travel-auth-anomaly-engi.vercel.app)
Account-takeover and attack-IP models trained on the 31.3M-login RBA dataset, plus a
physical impossible-travel check.
- On 5.4M held-out logins, it catches 14 of 22 account takeovers while challenging 0.77%
  of logins (ROC-AUC 0.978).
- A second model flags attack-IP logins (ROC-AUC 0.749).
- FastAPI · scikit-learn · DuckDB

**[Phishing URL detection](https://github.com/UtkarshOver9000/phishvpn-detection)** · [live demo](https://phishvpn-detection-ochre.vercel.app)
Trained on PhiUSIIL (235,795 URLs) plus the Tranco top-1M.
- Catches 63.2% of phishing domains live on the day of testing (OpenPhish), with 9 false
  alarms per 10,000 real sites.
- Includes an audit showing why this dataset's well-known ~100% scores are a URL-format
  shortcut.
- scikit-learn · FastAPI

**[Scam Site Detector](https://github.com/UtkarshOver9000/scam-site-detector)**
Browser extension with rule-based page scoring, measured on 235,795 real pages: few false
alarms, low recall. The numbers are why the phishing model above exists.
- TypeScript · Chrome extension API

### Energy (Smart India Hackathon 2026)

**[AETHERGRID Ω](https://github.com/UtkarshOver9000/aethergrid-omega)**
Uncertainty-aware demand optimisation for smart buildings: quantile forecasting, MPC and a
safety shield.
- The forecaster, run on 84 real Uttar Pradesh households (CEEW smart meters), cuts
  day-ahead feeder scheduling error by 11.7% against the best naive method.
- LightGBM · PuLP · Gymnasium · Streamlit

**[AETHERGRID World Sim](https://github.com/UtkarshOver9000/aethergrid-worldsim)** · [live 3D demo](https://aethergrid-worldsim.vercel.app)
24-society electricity district in the browser. It ships with a reality check against real
household meter data.
- Python · Three.js

### Retrieval and forecasting

**[AI Research Copilot](https://github.com/UtkarshOver9000/ai-research-copilot)** · [live demo](https://ai-research-copilot-3jwt.vercel.app)
Citation-first document Q&A.
- BM25 tuned on BEIR SciFact reaches nDCG@10 0.663 on held-out claims, nearly double the
  previous LSA retriever's 0.348.
- FastAPI · Next.js

**[Stock Price Movement Predictor](https://github.com/UtkarshOver9000/Stock-price-predictor)** · [dashboard](https://gcsrmstockpricepredictor-seven.vercel.app)
Next-day direction for 12 US stocks over 104,565 trading days of full history.
- No model beats a constant guess with statistical significance (every p > 0.17). The
  project documents why.

**[Crypto Surge Prediction](https://github.com/UtkarshOver9000/crypto-surge-prediction)**
Nine years of Binance data for 100 coins.
- Technical indicators don't predict 7-day +15% surges: test ROC-AUC 0.53, and the signal
  loses to random picks in a fee-adjusted backtest. They do carry a modest volatility
  signal (ROC-AUC 0.60).

### Community

**[F.A.S.T](https://github.com/UtkarshOver9000/F.A.S.T-website)** · [site](https://f-a-s-t-website-one.vercel.app)
Website for the Futuristic AI Society of Tech, an NVIDIA Student Developer Ecosystem
community at SRMIST Kattankulathur.

## Tools used in these projects

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?logo=javascript&logoColor=F7DF1E)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-2E7D32)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?logo=duckdb&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)
![Three.js](https://img.shields.io/badge/Three.js-000000?logo=threedotjs&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?logo=vercel&logoColor=white)

## About

I like problems where the honest answer matters more than the impressive one. Open to
collaborating on ML, security and energy projects.
