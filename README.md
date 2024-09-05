# DFT Sequence Plotter

This Python script plots the Discrete Fourier Transform (DFT) of a sequence alongside the sequence itself.

## Initializing

To specify a sequence `x[n]`, modify the array `x` in the script before running it.

### Buttons
- **Print Button**: Prints the current values of `x[n]`, `X[k]`, and the phases of `X[k]` on the terminal.
- **Reset Button**: Resets all values of `x[n]` to `0`.

## Plot Details

The script generates two subplots:

### A. Subplot 1: Sequence Plot
1. **Blue markers** represent the values of `x[n]` at each `n`.
2. **Grey markers** represent the average of the neighboring points, calculated as `(x[n+1] + x[n-1]) / 2` at each `n`.
3. **Interactive features:**
   - Click on any point to change the value of `x[n]`.
   - Click and drag any point to adjust its value. If the "Shift" key is not pressed, the marker snaps to the nearest integer.

### B. Subplot 2: DFT Plot
1. **Green markers** show the signed magnitude of `X[k] = DFT(x[n])`.
2. **Red markers** indicate the phase of `X[k]`. This helps identify negative values, as the phase of the corresponding `X[k]` will be `π`.
3. **Grey markers** represent the average `(X[0] + X[2*k]) / 2` at each `k`. This helps assess the stability of the eigenvalue represented by `X[k]` at the `k-th` mode. Generally, if the twisted state is larger than this grey marker, it can be considered stable.

