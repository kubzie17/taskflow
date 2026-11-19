# Optional fault — Why did the candidate refuse to start

**Ten minutes, only after both main workshops are complete.**

A colleague has prepared a local candidate with an identity path pointing to a file that is absent. Northbridge wants the reason identified and the configuration repaired before that candidate can be released.

Use the completed protected application in your local Python environment. Keep the cloud deployment running while you investigate locally. The trainer supplies a private disposable identity and database folder through the fallback instructions.

In a separate local PowerShell terminal, set `APP_ENVIRONMENT` to `local`, `TASKFLOW_DB` to an absolute path inside that existing disposable data directory, and `TASKFLOW_IDENTITY_FILE` to an absent file in that same private folder. Run the factory locally on port 18056.

```powershell
python -m uvicorn exercises.day09_entry:application --factory --host 127.0.0.1 --port 18056 --no-access-log
```

Find the first useful message, explain why the app has refused to start, repair the configured path and verify the protected routes using the provided probe on port 18056. Record the failure, correction and successful check. Keep the fictional identity file outside Git and the Docker build context.

Ask for a hint only after recording your initial diagnosis. Use the runtime-configuration section of the separate hints file. A stretch is to explain how the same missing path differs from a denied `ssm:GetParameter` permission.
