# ZeladorX engineering rules

- Keep the shared corporate data model and shared-app migrations compatible with ChatChannels and the API repository, because all three products use the same database.
- Extend AdminLTE through `setup/static/dist/css/zeladorx-modern.css` and `setup/static/dist/js/zeladorx-modern.js`, because replacing vendor files makes upgrades and troubleshooting unsafe.
- Keep sidebar expansion state in browser UI state only, because navigation preferences must not require database changes.
