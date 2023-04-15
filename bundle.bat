@echo off

call conda activate GiGaia

:: pyinstaller bundle_client.py --distpath "bundled" --workpath "bundler_wp" -i NONE --key GIGGIG2023 --noconsole --onefile -n "GiGaia"

python -m GiGaiaBundler

pause
