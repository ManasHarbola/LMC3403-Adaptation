# Appendix A: CHIP-8 Instruction Reference
**Notes**

The notation _Vx_ or _Vy_ refers to any general-purpose register (i.e. registers 0 through F). The notation for other registers is as follows:
- `I` - memory address register
- `PC` - program counter register
- `SP` - stack pointer register
- `DT` - delay timer register
- `ST` - sound timer register.

Additionally, _nnn_ refers to some memory address, and _kk_ refers to some constant byte value.

Many instructions have multiple versions. The format and semantics (in both English and C-style pseudocode) of each are listed.

### `ADD` - Addition
- `7xkk - ADD Vx, kk` : Adds the byte _kk_ to the value in _Vx_. The result is stored in _Vx_.
    - `Vx = Vx + kk;`
- `8xy4 - ADD Vx, Vy` : Adds the value in _Vy_ to the value in _Vx_. The result is stored in _Vx_; _Vy_ is unaffected.
    - `Vx = Vx + Vy;`
- `Fx1E` : Adds the value in _Vx_ to memory address register `I`. The result is stored in `I`; _Vx_ is unaffected.
    - `I = I + Vx;`

### `AND` - Bitwise AND
- `8xy2 - AND Vx, Vy` : Performs a bitwise AND of the values in _Vx_ and _Vy_. The result is stored in _Vx_; _Vy_ is unaffected.
    - `Vx = Vx & Vy;`

### `BCD` - Binary-coded decimal
- `Fx33 - BCD Vx` : Stores the digits of the decimal representation of the value in _Vx_ into three memory locations starting at the address in `I`.
    - `*I = hundreds_digit(Vx); *(I+1) = tens_digit(Vx); *(I+2) = ones_digit(Vx);`

### `CALL` - Call subroutinue
- `2nnn - CALL nnn` : Pushes the current value of `PC` onto the top of the stack, and sets `PC` to _nnn_.
    - `SP = SP + 1; stack[SP] = PC; PC = nnn;`

### `CLS` - Clear screen
- `00E0 - CLS` : Clears the screen
    - `clear_screen();`

### `DRW` - Draw sprite
- `Dxyn - DRW Vx, Vy, n` : Draws the _n_ byte sprite located at the address in `I` on the screen, at coordinates (_Vx_, _Vy_). Drawing is done using XOR, and _VF_ is set if any pixels are cleared in the process. Drawing is also done in a wrap-around fashion, so any part of the sprite that would be placed outside of the display boundaries is drawn on the opposite side.
    - `draw_sprite(Vx, Vy, I, n);`

### `JP` - Jump
- `1nnn - JP nnn` : Sets `PC` to the address _nnn_.
    - `PC = nnn;`
- `Bnnn - JP V0, nnn` : Sets `PC` to the sum of the value in _V0_ and _nnn_.
    - `PC = V0 + nnn;`

### `LD` - Load
- `6xkk - LD Vx, kk` : Loads the byte value _kk_ into _Vx_.
    - `Vx = kk;`
- `8xy0 - LD Vx, Vy` : Loads the value in _Vy_ into _Vx_. _Vy_ is unaffected.
    - `Vx = Vy;`
- `Annn - LD I, nnn` : Loads the address _nnn_ into `I`.
    - `I = nnn;`
- `Fx07 - LD Vx, DT` : Loads the value of `DT` into _Vx_. The value of the delay timer is unaffected.
    - `Vx = DT;`
- `Fx0A - LD Vx, K` : Loads the value of the next pressed key into _Vx_. Program execution is halted until a key is pressed.
    - `Vx = get_next_key();`
- `Fx15 - LD DT, Vx` : Loads the value in _Vx_ into `DT`. _Vx_ is unaffected.
    - `DT = Vx;`
- `Fx18 - LD ST, Vx` : Loads the value in _Vx_ into `ST`. _Vx_ is unaffected.
    - `ST = Vx;`
- `Fx55 - LD I, Vx` : Loads the registers _V0_ through _Vx_ into the memory locations starting at the address in `I`. All registers are unaffected.
    - `*I = V0; *(I+1) = V1; ...; *(I+x) = Vx;`
- `Fx65 - LD Vx, I` : Loads the values in memory starting at the address in `I` into registers _V0_ through _Vx_. All memory locations are unaffected.
    - `V0 = I[0]; V1 = I[1]; ...; Vx = I[x];`

### `LDF` - Load font
- `Fx29 - LDF Vx` : Loads the location of the hexadecimal sprite corresponding to the value in _Vx_ into `I`.
    - `I = hex_sprites[Vx];`

### `OR` - Bitwise OR
- `8xy1 - OR Vx, Vy` : Performs a bitwise OR of the values in _Vx_ and _Vy_. The result is stored in _Vx_; _Vy_ is unaffected.
    - `Vx = Vx | Vy;`

### `RET` - Return from subroutinue
- `00EE - RET` : Removes and sets the program counter to the top-most address on the stack.
    - `PC = stack[SP]; SP = SP - 1;`

### `RND` - Random value
- `Cxkk - RND Vx, kk` : Generates a random byte, then performs a bitwise AND between it and _kk_. The result is stored in _Vx_.
    - `Vx = rnd() & kk;`

### `S` - Skip next instruction
- `3xkk - SE Vx, kk` : Skips the next instruction if _Vx_ has the value _kk_.
    - `PC = (Vx == kk ? (PC + 2) : (PC + 1));`
- `4xkk - SNE Vx, kk` : Skips the next instruction if _Vx_ does not have the value _kk_.
    - `PC = (Vx != kk ? (PC + 2) : (PC + 1));`
- `5xy0 - SE Vx, Vy` : Skips the next instruction if _Vx_ and _Vy_ have the same values.
    - `PC = (Vx == Vy ? (PC + 2) : (PC + 1));`
- `9xy0 - SNE Vx, Vy` : Skips the next instruction if _Vx_ and _Vy_ do not have the same values.
    - `PC = (Vx != Vy ? (PC + 2) : (PC + 1));`
- `Ex9E - SKP Vx` : Skips the next instruction if the key with the same value as _Vx_ is pressed.
    - `PC = (key_pressed(Vx) ? (PC + 2) : (PC + 1));`
- `ExA1 - SKNP Vx` : Skips the next instruction if the key with the same value as _Vx_ is not pressed.
    - `PC = (!key_pressed(Vx) ? (PC + 2) : (PC + 1));`

### `SH` - Bitwise shift
- `8xy6 - SHR Vx` : Sets _VF_ to the value of the least significant bit of the value in Vx, then shifts the value in _Vx_ right by one bit. The result is stored in _Vx_.
    - `VF = Vx & 1; Vx = Vx >> 1;`
- `8xyE - SHL Vx` : Sets _VF_ to the value of the most significant bit of the value in Vx, then shifts the value in _Vx_ left by one bit. The result is stored in _Vx_.
    - `VF = msb(Vx); Vx = Vx << 1;`

### `SUB` - Subtraction
- `8xy5 - SUB Vx, Vy` : Subtracts the value in _Vy_ from the value in _Vx_. The result is stored in _Vx_; _Vy_ is unaffected. If the result would be negative, _VF_ is set to 1; otherwise, it is set to 0.
    - `Vx = Vx - Vy;`
- `8xy7 - SUBN Vx, Vy` : Subtracts the value in _Vx_ from the value in _Vy_. The result is stored in _Vx_; _Vy_ is unaffected. If the result would be negative, _VF_ is set to 1; otherwise, it is set to 0.
    - `Vx = Vy - Vx;`

### `SYS` - System call [DEPRECATED]
- `0nnn - SYS nnn` : Jumps to machine code subroutinue at address _nnn_. This instruction is deprecated, and ignored by most modern emulators.
    - `PC = nnn;`

### `XOR` - Bitwise XOR
- `8xy3 - XOR Vx, Vy` : Performs a bitwise exclusive OR (XOR) of the values in _Vx_ and _Vy_. The result is stored in _Vx_; _Vy_ is unaffected.
    - `Vx = Vx ^ Vy;`