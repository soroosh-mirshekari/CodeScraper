# CodeScraper  
Real Estate Advertisement Aggregation and Similarity Analysis

## Overview
CodeScraper is a modular Python-based system designed to collect, clean, and analyze
real estate advertisements from multiple online platforms with heterogeneous and
frequently changing data formats.

## Objective
The goal of this project is to build an end-to-end pipeline that:
- aggregates listings from different sources,
- normalizes noisy and unstructured textual data,
- identifies potentially duplicate or related advertisements,
- and stores structured results for further analysis.

## Approach
The system is designed in a modular and extensible manner:
- platform-specific scraping modules handle source-dependent structures,
- a preprocessing pipeline performs text normalization and data cleaning,
- a similarity analysis module compares independent listings,
- and a relational database layer manages persistent storage.

The design emphasizes robustness against incomplete data and evolving page structures.

## Key Concepts
Web scraping without official APIs • text preprocessing • string similarity analysis •
modular object-oriented design • relational databases

## Project Structure
- `main.py`: main orchestration and execution flow  
- `database_manager.py`: database connection and persistence logic  
- `similarity_algorithm.py`: similarity computation between advertisements  
- source-specific modules for scraping and cleaning  

## How to Run
1. Install required dependencies  
2. Configure database settings if needed  
3. Run the main script:
   ```bash
   python main.py
