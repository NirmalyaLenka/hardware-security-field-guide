# FAQ

**Do I need expensive equipment to start?**
No. Levels 1–2 and Lab 01 need only a dev board (~$5–10), a multimeter (~$15), and a USB-to-UART adapter if your board doesn't have one built in. Levels 3–4 add a logic analyzer and a flash programmer, each roughly $5–25.

**Is this guide only about attacking devices?**
No. Most techniques here are diagnostic (reading a boot log, dumping firmware, measuring a voltage) and are equally useful for debugging your own embedded projects as for security analysis. [Safety and Authorized Use](safety/index.md) explains the authorization boundary for anything beyond your own hardware.

**Can I use this guide's techniques on a device I bought but didn't build?**
Generally yes, for your own personal unit, within the limits in [Safety and Authorized Use](safety/index.md) — but be aware that disassembling a device may void its warranty, and redistributing any proprietary firmware you extract may violate the vendor's license even when your analysis is legitimate.

**Why doesn't this guide cover [some topic] yet?**
See the honest status note at the bottom of the [Learning Path](learning-path.md) — this release prioritizes a small number of complete, verified guides over a larger number of thin ones. Contributions are welcome; see `CONTRIBUTING.md` at the project root.

**How do I report a mistake in a guide?**
Open an issue describing the page, the claim, and why you believe it's incorrect — ideally with a reference. See `CONTRIBUTING.md` at the project root.
