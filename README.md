# AI Coding Agent

A Python-based AI agent that can analyze, debug, and modify codebases using Google's Gemini API.

## Description

This project implements an AI coding agent that can:
- Analyze code files and understand project structure
- Debug and fix code issues
- Suggest improvements and refactoring
- Add new features to existing codebases

## Warning

This agent is able to write files and execute python scripts, which are cointained in a working directory. For security reasons, the working directory is hard coded in call_function.py. Still, it probably is NOT completly safe to use this agent!