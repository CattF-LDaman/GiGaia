@echo off

call conda activate GiGaia

pyinstaller run_client.py --distpath "bundled" --workpath "bundler_wp" -i NONE --key GIGGIG2023 --noconsole --onefile -n "GiGaia"

pause
