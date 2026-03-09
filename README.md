# Reporte Mensual de Mazos

[![Quarto](https://img.shields.io/badge/Quarto-1.6+-00BFAE?style=for-the-badge&logo=quarto&logoColor=white&labelColor=101010)](https://quarto.org)
[![R](https://img.shields.io/badge/R-4.4+-276DC3?style=for-the-badge&logo=r&logoColor=white&labelColor=101010)](https://www.r-project.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6+-00a393?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=101010)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-8.0+-00684A?style=for-the-badge&logo=mongodb&logoColor=white&labelColor=101010)](https://www.mongodb.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-00BFFF?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=101010)](https://www.postgresql.org)

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-monthly_report_YGO_Duel_Links-00BFAE?style=for-the-badge&logo=github&logoColor=white)](https://luceldasilva.github.io/monthly_report_YGO_Duel_Links/)

[![Deploy en Vercel](https://img.shields.io/badge/Vercel-Running-brightgreen?style=for-the-badge&logo=vercel)](https://monthly-report-yugioh-dl.vercel.app)

Desplegada la base de datos en
[![Static Badge](https://img.shields.io/badge/build-neon.tech-brightgreen?logo=postgresql&label=serverless&labelColor=%23AFEEEE&color=%237ff9c7)](https://neon.tech)

## Problema
Los creadores de contenido necesitaban analizar el meta mensual del videojuego [Yu-Gi-Oh! Duel Links](https://www.konami.com/yugioh/duel_links/en) y que están usando actualmente sus comunidades, pero recopilar y visualizar los datos tomaba mucho tiempo.

## Solución
Construí un pipeline de datos y generé visualizaciones automatizadas para mostrar los decks más utilizados que llegan al rango King of Games y Dlv. MAX de sus copas KC.

Hago la recopilación de los datos en las comunidades de los siguientes creadores de contenido:

[![](https://img.shields.io/youtube/channel/subscribers/UCntaHPDpcJgDRNf_W_DETkA?label=Zerotg&logo=youtube&style=for-the-badge)](https://www.youtube.com/@ZeroTG) [![](https://img.shields.io/youtube/channel/subscribers/UCBrumTmd9VbSW0mWesf8czw?label=zephracarl&logo=youtube&style=for-the-badge)](https://www.youtube.com/@ZephraCarl) [![](https://img.shields.io/youtube/channel/subscribers/UCv041WoJ7kTVyXsD4pctvOw?label=bryan%20nor%C3%A9n&logo=youtube&style=for-the-badge)](https://www.youtube.com/@BryanNoren)   
[![](https://img.shields.io/youtube/channel/subscribers/UCSJhvpXNChrL18yL3ROfiiQ?label=xenoblur&logo=youtube&style=for-the-badge)](https://www.youtube.com/@XenoBlur) [![](https://img.shields.io/youtube/channel/subscribers/UCjsHwfYzlxzUnXTVxAXlwsw?style=for-the-badge&logo=youtube&label=Yami%20Glen)](https://www.youtube.com/@YamiGlen) [![](https://img.shields.io/youtube/channel/subscribers/UCb2IY1R6rLzjMgx3IUtfRHA?style=for-the-badge&logo=youtube&label=Yam_VT)](https://www.youtube.com/@Yam_VT)

## Resultado
Pudieron preparar sus videos más rápido, ahorrando aproximadamente 1 hora de trabajo por video.


![](https://monthly-report-yugioh-dl.vercel.app/reports/latino_vania.png)

## Extras
Si quieres ejecutar este repositorio, puedes clonarlo y crear un ambiente virtual del que prefiera e instálelo con este comando
```bash
pip install -r requirements.txt && pip install -e . --use-pep517
```

Si usará R y entorno conda puede usar este comando
```bash
conda install -c conda-forge r-essentials r-calendR r-styler r-glue r-here
```
