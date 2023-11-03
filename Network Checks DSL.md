Here's the formal description of the DSL for defining network behavior checks:

### DSL for Network Behavior Checks

1. **Program Entry**:
   - Each program is represented by its name (e.g., "sshd", "xrdp", "chrome").
   - Each program entry has a description and a link
   - Each program entry contains a list of checks.

2. **Check Descriptions**:
   
   a. **Check Listening Ports**:
      - Format: `LISTEN_ON:<port_number>`
      - Purpose: Verifies that a program is listening on a specific port.
      - Example: `LISTEN_ON:22`
   
   b. **No Listening Ports**:
      - Format: `NO_LISTEN`
      - Purpose: Ensures that a program is not listening on any port.
      - Example: `NO_LISTEN`
   
   c. **Validate Expected Connections**:
      - Format: `VALIDATE_CONN:local=[<local_addresses>]:<local_port>;remote=[<remote_addresses>]:<remote_port>`
      - Purpose: Checks if all connections on certain allowed local and/or remote addresses are using a specific port.
      - Notes:
         - Local and remote addresses are enclosed in square brackets (`[]`).
         - Multiple addresses can be separated by commas.
         - Local and remote specifications are separated by a semi-colon `;`.
         - Either local or remote specifications can be omitted.
      - Examples:
         - Only local host:port validation: `VALIDATE_CONN:local=[0.0.0.0,::]:22`
         - Both local and remote host:port validation: `VALIDATE_CONN:local=[0.0.0.0]:22;remote=[192.168.1.5]:80`
         - Only remote host:port validation: `VALIDATE_CONN:remote=[192.168.1.5]:80`
   
   d. **Non-System User**:
      - Format: `NON_SYS_USER`
      - Purpose: Ensures that a program is not being run by a system user (typically, user IDs below 1000 are considered system users).
      - Example: `NON_SYS_USER`

   e. **System User**:
      - Format: `SYS_USER`
      - Purpose: Ensures that a program is being run by a system user (typically, user IDs below 1000 are considered system users).
      - Example: `SYS_USER`

   f. **Validate Username**:
      - Format: `VALIDATE_USERNAME`
      - Purpose: Ensures that a program is being run by a specific user.
      - Example: `VALIDATE_USERNAME:postgres`

   g. **Validate UID**:
      - Format: `VALIDATE_UID`
      - Purpose: Ensures that a program is being run by a specific user id.
      - Example: `VALIDATE_UID:129`

### Notes:
- The DSL is designed to be machine-readable, making it easier to parse and execute checks programmatically.
- Square brackets (`[]`) are used to handle potential ambiguity introduced by IPv6 addresses, which also contain colons.
- Semi-colons `;` are used to separate local and remote specifications, ensuring clarity and avoiding parsing issues.
- Each check description is independent and can be parsed separately.

This updated formal description provides a structured overview of the DSL, incorporating the modifications made during our discussion.