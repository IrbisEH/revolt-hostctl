# revolt-hostctl

`revolt-hostctl` is a lightweight CLI tool for managing hosts and networks in small-scale infrastructure environments.

The project aims to provide a simple, structured way to:

- manage hosts and networks
- persist configuration locally
- operate through a clean command-line interface
- keep infrastructure state transparent and reproducible

## Configuration, Logs, and Storage

### Data Location
All application data (configuration, logs, and database) is stored in the standard user data directory, which depends on the operating system (the `platformdirs` library is used):
- **Linux:** `~/.local/share/revolt-hostctl`
- **macOS:** `~/Library/Application Support/revolt-hostctl`
- **Windows:** `C:\Users\<User>\AppData\Local\revolt-hostctl`

### Configuration
The application uses a `.env` file located in the root data directory (see above). An empty file is created on the first run. You can customize the application's behavior by adding environment variables to this file.

#### Available Options

| Variable | Description | Default Value |
| :--- | :--- | :--- |
| `LOG_LEVEL` | Logging level (`debug`, `info`, `warning`, `error`, `critical`) | `DEBUG` |
| `LOG_MAX_BYTES` | Maximum size of a single log file in bytes | `5242880` (5MB) |
| `LOG_BACKUP_COUNT` | Number of old log files to keep | `5` |
| `LOG_CONSOLE` | Duplicate logs to console (stdout) (`0` - no, `1` - yes) | `0` |