# Threat Modeling for a Hardware/IoT Device

## 1. What is this?

A structured way of asking "what could go wrong, for whom, and how badly" about a piece of hardware, before you start poking at it. It turns an unfocused "is this secure?" into a specific, answerable list.

## 2. Why does it matter?

Without a threat model, testing becomes a grab-bag of random checks. With one, you can say precisely what you tested, what you didn't, and why a given weakness does or doesn't matter for this device's actual use.

## 3. How does it work?

A lightweight hardware threat model answers four questions:

1. **Assets** — what is worth protecting? (e.g., Wi-Fi credentials stored in flash, a signing key, the integrity of sensor readings, physical safety if the device controls something mechanical.)
2. **Attack surface** — what can an attacker touch? (Network interfaces, a UART/JTAG header, a removable SD card, a companion mobile app's API, physical access to the device itself.)
3. **Trust boundaries** — where does trust change hands? (Between the cloud service and the device, between the device's bootloader and its application firmware, between an unauthenticated local network and the device.)
4. **Attacker capability and authorization** — what can a realistic, *authorized* tester (you, testing your own device) actually do, and what does "success" look like for a specific check? (e.g., "Can an attacker with physical access for 60 seconds extract the Wi-Fi password?" is answerable; "is this hackable?" is not.)

This produces a short table rather than a vague narrative:

| Asset | Surface | Trust boundary crossed | Example check |
|---|---|---|---|
| Wi-Fi password | Exposed UART console | Debug interface → application memory | Does the console require authentication before showing stored config? |
| Firmware integrity | OTA update mechanism | Cloud → device | Is the update image signature-verified before flashing? |
| Physical safety | Relay output controlling mains device | Firmware bug → physical actuator | Can a malformed network packet cause the relay to toggle unexpectedly? |

## 4. What do you need?

- A clear statement of which device, which firmware version, and which interfaces are in scope.
- Written authorization if the device is not solely your own (even a simple statement is enough for personal/lab use; formal authorization is required for anything beyond that).
- No special tools — this is a planning exercise done before any hands-on testing.

## 5. How do you do it?

1. List every physical and network interface the device exposes (count the ports, headers, and radios — don't rely on the datasheet alone; verify against the physical board).
2. For each interface, write one sentence describing what crossing it would let someone do.
3. Mark which interfaces are reachable without physical access (network/radio) versus which require physical possession of the device (UART, JTAG, flash chip).
4. Prioritize: an unauthenticated network-reachable issue is usually more impactful than one requiring disassembly, but weigh this against the device's actual deployment (a UART header is a bigger deal on a device meant to be tamper-resistant than on a hobbyist dev board).
5. Turn each row into a specific, testable question before moving to the practical labs.

## 6. What should happen?

You should end with a short table (5–15 rows is typical for a simple device) of concrete, testable statements — not a general impression of "secure" or "insecure."

## 7. What can go wrong?

| Symptom | Likely cause | Fix |
|---|---|---|
| The table only has one or two rows | Surface enumeration was too shallow | Physically inspect the board for unpopulated headers and test points, not just documented interfaces |
| Every row says "could be hacked" | Questions are not specific enough | Rewrite each row as a yes/no question with a defined test procedure |

## 8. Safety and limitations

- A threat model is a planning tool, not a guarantee — it does not replace the safety and authorization requirements in [Safety and Authorized Use](../safety/index.md).
- Do not threat-model, and do not test, devices you do not own or do not have explicit, documented permission to examine.

## 9. Verification status

Reviewed methodology, not independently hardware-tested (this page is a process guide rather than a hands-on procedure). The example table was built against a real device (a network-controlled relay module owned by the author) during documentation review, November 2026.

> **Repository validation (2026-11-24): PASS — 0 errors in the local checks completed for this package.** The run passes 9 link-checker regression tests, checks 21 Markdown files with 0 broken internal links, compiles all Python under `scripts/`, `examples/`, and `tests/`, and parses both YAML files. The strict MkDocs build passed locally in 3.19 seconds; Material for MkDocs emitted a non-fatal compatibility warning about future MkDocs 2.0 changes. GitHub Actions has not yet been verified on GitHub-hosted infrastructure. See `tests/verification-report.md` at the repository root for exact scope. This repository-level result does not mean every hardware variant or operating-system instruction has been physically tested.

## 10. References

- OWASP, "IoT Security Testing Guide" (general threat-modeling structure; adapted here, not reproduced).
- NIST IR 8259, "Foundational Cybersecurity Activities for IoT Device Manufacturers," for asset/boundary framing concepts.
