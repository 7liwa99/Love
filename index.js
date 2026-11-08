// Frame control settings
const FPS = 30;
let lastTime = performance.now();

// Ported Math Utilities
function clamp(v, lo = 0.0, hi = 1.0) {
    return v < lo ? lo : (v > hi ? hi : v);
}

function mix(a, b, k) {
    return [
        a[0] + (b[0] - a[0]) * k,
        a[1] + (b[1] - a[1]) * k,
        a[2] + (b[2] - a[2]) * k
    ];
}

// Convert your normalized RGB float arrays directly into CSS string values
function hexc(c) {
    let r = Math.floor(clamp(c[0]) * 255);
    let g = Math.floor(clamp(c[1]) * 255);
    let b = Math.floor(clamp(c[2]) * 255);
    return `rgb(${r},${g},${b})`;
}

// Main browser render tick loop (Replaces root.after(100, tick))
function tick(now) {
    let dt = clamp((now - lastTime) / 1000.0, 0.0, 0.1);
    lastTime = now;
    
    // 1. Process your timeline states (T_BURN, T_SPREAD, etc.)
    // 2. Compute heat arrays and particle positions 
    // 3. Build the composite string out of characters with color tags
    
    requestAnimationFrame(tick);
}

// Start the animation loop
requestAnimationFrame(tick);
