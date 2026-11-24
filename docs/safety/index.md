# Safety and Authorized Use

## Scope

Every practical exercise in this guide assumes you are working on hardware you own, or on hardware you have explicit, documented permission to examine. This applies without exception to UART/JTAG probing, firmware extraction, protocol sniffing, and every lab in this repository.

## What this guide does not cover

- Gaining access to a device without the owner's permission.
- Defeating protections on a device you do not own, including devices provided by an employer or client without a written authorization scope.
- Deploying modified or malicious firmware to any device other than your own test hardware.
- Any technique whose primary purpose is persistence, credential theft, or interference with a system that is not yours.

Where a technique in this guide has genuine dual use (for example, understanding default credentials is necessary both to find and to fix them), the guide explains its defensive purpose and its authorization boundary explicitly, rather than assuming the reader's intent.

## Electrical safety

- This guide covers low-voltage (typically ≤5V), battery- or USB-powered logic electronics only. It does not cover mains-voltage work.
- Confirm a device's rated voltage before connecting any external power or signal source to it.
- Disconnect power before placing or moving physical test probes.
- If a procedure can alter a device's stored firmware or configuration, treat it as destructive until proven otherwise, and have a recovery plan (a second firmware dump, a known-good backup) before you start.

## Responsible disclosure

If, while working on a device, you discover a vulnerability that affects other users of the same product (not just your personal unit), follow a coordinated disclosure process: contact the vendor privately first, give them reasonable time to respond, and avoid publishing exploit details that would put other users at risk before a fix is available. `CONTRIBUTING.md` at the project root explains how to contribute writeups of this kind to the project once a fix is public.

## If you are unsure

If you are not sure whether you are authorized to test a specific device or network, stop and get explicit written permission first. None of the material in this repository is a substitute for that permission.
