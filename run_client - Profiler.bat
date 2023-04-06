@echo off

call conda activate GiGaia

python -m cProfile -o profiler_results.dat run_client.py
snakeviz profiler_results.dat

pause