#  kAI — AI Menu Generator (Backend)

**Backend & AI service** that generates **diverse, nutritious, $3 lunchbox menus** to help reduce food waste in New Zealand’s free school lunch program.

- **Role:** Backend & AI Developer  
- **Year:** 2025  
- **Stack:** Django · Django REST Framework · PostgreSQL · OpenAI GPT  
- **Frontend demo:** https://kai-happytummy.vercel.app/

> This repository contains the **Django/DRF API**. The React (Tailwind) frontend lives in a separate app (see demo above).

---

## Overview

Built as a 48-hour AI Hackathon MVP, **kAI** tackles high food waste (≈70%) in the government-funded school lunch program, driven by repetitive and uninspiring menus.  
The service generates **monthly meal plans** within a **$3 per lunchbox** budget while respecting **dietary requirements**, **calorie/nutrition guidance**, and **available inventory/budget** constraints.

### What it does
- Generates **monthly menus** for schools under strict budget
- Supports **dietary filters** (vegetarian, halal, gluten-free)
- Is **calorie/nutrition-aware** in prompts (aligned with dietary standards)
- Incorporates **available inventory** and **student counts**

---

## Features

- ✅ AI-generated monthly menus within a **$3 budget**  
- ✅ Customization by **dietary requirements** (vegetarian / halal / gluten-free)  
- ✅ **Calorie/nutrition-aware** prompt design  
- ✅ Uses **available inventory** & budget constraints to optimize plans  
- ✅ RESTful API for frontend integration (React/Tailwind)  

---

## Tech Stack

- **Backend:** Django, Django REST Framework  
- **DB:** PostgreSQL (SQLite supported for local dev)  
- **AI:** OpenAI GPT (server-side prompting)  
- **Other:** Python 3.10+, pip/venv

## Screenshots
![Screenshot](kai-0.png)
![Screenshot](kai-1.png)
![Screenshot](kai-2.png)
![Screenshot](kai-4.png)


## Outcome

Delivered a functional MVP within 48 hours at an AI Hackathon:
AI-generated menus that are cost-efficient, nutritious, and tailored to dietary needs and available resources—demonstrating potential to reduce food waste and improve student satisfaction.