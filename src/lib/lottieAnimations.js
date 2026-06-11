// Easing Curves (snappy custom curves resembling Apple UI animations)
const ease1D = {
  i: { x: [0.25], y: [1.0] },
  o: { x: [0.25], y: [0.0] }
};

const ease3D = {
  i: { x: [0.25, 0.25, 0.25], y: [1.0, 1.0, 1.0] },
  o: { x: [0.25, 0.25, 0.25], y: [0.0, 0.0, 0.0] }
};


const transform = ({ x = 100, y = 100, scale = [100, 100, 100], rotation = 0, opacity = 100 } = {}) => {
  const isScaleAnimated = Array.isArray(scale) && typeof scale[0] === 'object';
  const isRotationAnimated = Array.isArray(rotation) && typeof rotation[0] === 'object';
  return {
    o: { a: 0, k: opacity },
    r: isRotationAnimated
      ? { a: 1, k: rotation }
      : { a: 0, k: rotation },
    p: { a: 0, k: [x, y, 0] },
    a: { a: 0, k: [0, 0, 0] },
    s: isScaleAnimated
      ? { a: 1, k: scale }
      : { a: 0, k: scale }
  };
};

// Color interpolation for a premium paper palette (Terracotta -> Craft Gold -> Slate Blue -> Warm Sand)
const interpolateColor = (index, total) => {
  const t = index / (total - 1);
  // Muted paper color stops:
  // t = 0.0: Terracotta    [0.81, 0.34, 0.13, 1]
  // t = 0.33: Craft Gold   [0.89, 0.60, 0.20, 1]
  // t = 0.66: Slate Blue   [0.29, 0.49, 0.57, 1]
  // t = 1.0: Warm Sand     [0.86, 0.71, 0.46, 1]
  if (t < 0.33) {
    const localT = t / 0.33;
    return [
      0.81 + localT * 0.08,
      0.34 + localT * 0.26,
      0.13 + localT * 0.07,
      1
    ];
  } else if (t < 0.66) {
    const localT = (t - 0.33) / 0.33;
    return [
      0.89 - localT * 0.60,
      0.60 - localT * 0.11,
      0.20 + localT * 0.37,
      1
    ];
  } else {
    const localT = (t - 0.66) / 0.34;
    return [
      0.29 + localT * 0.57,
      0.49 + localT * 0.22,
      0.57 - localT * 0.11,
      1
    ];
  }
};

// --- EQUALIZER SINE WAVE GENERATOR ---
const generateWaveBars = () => {
  const totalBars = 24;
  const layers = [];
  const barWidth = 3.5;
  const gap = 12;
  const startX = 22;
  
  for (let i = 0; i < totalBars; i++) {
    const x = startX + i * gap;
    const y = 130;
    
    // Wave height based on sine wave pattern
    const phase = (i / totalBars) * Math.PI * 2.5;
    const baseHeight = 60 + Math.sin(phase) * 20;
    const delay = Math.round((i / totalBars) * 45); // offset delay to create a scrolling wave
    
    layers.push({
      ddd: 0,
      ind: i + 1,
      ty: 4,
      nm: `Wave bar ${i + 1}`,
      sr: 1,
      ks: transform({
        x,
        y,
        scale: [
          { t: 0, s: [100, 20, 100], e: [100, 125, 100], ...ease3D },
          { t: 15, s: [100, 125, 100], e: [100, 40, 100], ...ease3D },
          { t: 30, s: [100, 40, 100], e: [100, 110, 100], ...ease3D },
          { t: 45, s: [100, 110, 100], e: [100, 20, 100], ...ease3D },
          { t: 60, s: [100, 20, 100] }
        ]
      }),
      ao: 0,
      shapes: [
        {
          ty: 'rc',
          d: 1,
          s: { a: 0, k: [barWidth, baseHeight] },
          p: { a: 0, k: [0, -baseHeight / 2] }, // bottom anchor to scale upwards
          r: { a: 0, k: 1.5 }, // sleek pill shape
          nm: 'rounded bar'
        },
        {
          ty: 'fl',
          c: { a: 0, k: [1, 1, 1, 1] }, // premium monochrome white
          o: { a: 0, k: 80 }, // subtle opacity
          nm: 'fill'
        }
      ],
      ip: 0,
      op: 60,
      st: -delay, // Offset layer start time dynamically in frames
      bm: 0
    });
  }
  return layers;
};

export const wavePulse = {
  v: '5.12.0',
  fr: 30,
  ip: 0,
  op: 60,
  w: 320,
  h: 170,
  nm: 'Vibe Central wavePulse upgraded',
  ddd: 0,
  assets: [],
  layers: generateWaveBars()
};

// --- HIGH FIDELITY SPINNING VINYL RECORD ---
export const recordSpin = {
  v: '5.12.0',
  fr: 30,
  ip: 0,
  op: 90,
  w: 180,
  h: 180,
  nm: 'Vibe Central recordSpin upgraded',
  ddd: 0,
  assets: [],
  layers: [
    // 1. Vinyl Body (Large dark charcoal circle)
    {
      ddd: 0,
      ind: 1,
      ty: 4,
      nm: 'vinyl body',
      sr: 1,
      ks: transform({
        x: 90,
        y: 90,
        scale: [100, 100, 100]
      }),
      ao: 0,
      shapes: [
        { ty: 'el', p: { a: 0, k: [0, 0] }, s: { a: 0, k: [156, 156] }, nm: 'body circle' },
        { ty: 'fl', c: { a: 0, k: [0.08, 0.08, 0.08, 1] }, o: { a: 0, k: 100 }, nm: 'body fill' }
      ],
      ip: 0,
      op: 90,
      st: 0,
      bm: 0
    },
    // 2. Vinyl Grooves (Thin concentric white circles rotating)
    {
      ddd: 0,
      ind: 2,
      ty: 4,
      nm: 'grooves outer',
      sr: 1,
      ks: transform({
        x: 90,
        y: 90,
        rotation: [
          { t: 0, s: [0], e: [360], ...ease1D },
          { t: 90, s: [360] }
        ]
      }),
      ao: 0,
      shapes: [
        { ty: 'el', p: { a: 0, k: [0, 0] }, s: { a: 0, k: [136, 136] }, nm: 'groove circle' },
        { ty: 'st', c: { a: 0, k: [1, 1, 1, 1] }, o: { a: 0, k: 8 }, w: { a: 0, k: 1 }, nm: 'groove stroke' }
      ],
      ip: 0,
      op: 90,
      st: 0,
      bm: 0
    },
    {
      ddd: 0,
      ind: 3,
      ty: 4,
      nm: 'grooves middle',
      sr: 1,
      ks: transform({
        x: 90,
        y: 90,
        rotation: [
          { t: 0, s: [0], e: [360], ...ease1D },
          { t: 90, s: [360] }
        ]
      }),
      ao: 0,
      shapes: [
        { ty: 'el', p: { a: 0, k: [0, 0] }, s: { a: 0, k: [110, 110] }, nm: 'groove circle' },
        { ty: 'st', c: { a: 0, k: [1, 1, 1, 1] }, o: { a: 0, k: 7 }, w: { a: 0, k: 1 }, nm: 'groove stroke' }
      ],
      ip: 0,
      op: 90,
      st: -15, // Offset to add organic rotation difference
      bm: 0
    },
    {
      ddd: 0,
      ind: 4,
      ty: 4,
      nm: 'grooves inner',
      sr: 1,
      ks: transform({
        x: 90,
        y: 90,
        rotation: [
          { t: 0, s: [0], e: [360], ...ease1D },
          { t: 90, s: [360] }
        ]
      }),
      ao: 0,
      shapes: [
        { ty: 'el', p: { a: 0, k: [0, 0] }, s: { a: 0, k: [84, 84] }, nm: 'groove circle' },
        { ty: 'st', c: { a: 0, k: [1, 1, 1, 1] }, o: { a: 0, k: 6 }, w: { a: 0, k: 1 }, nm: 'groove stroke' }
      ],
      ip: 0,
      op: 90,
      st: -30,
      bm: 0
    },
    // 3. Crossed Reflection Highlights (bowtie light reflection rotating back-and-forth)
    {
      ddd: 0,
      ind: 5,
      ty: 4,
      nm: 'reflection highlights',
      sr: 1,
      ks: transform({
        x: 90,
        y: 90,
        rotation: [
          { t: 0, s: [-10], e: [15], ...ease1D },
          { t: 45, s: [15], e: [-10], ...ease1D },
          { t: 90, s: [-10] }
        ]
      }),
      ao: 0,
      shapes: [
        // Two crossed thin white rectangles with low opacity simulating linear reflection highlights
        {
          ty: 'rc',
          s: { a: 0, k: [142, 6] },
          p: { a: 0, k: [0, 0] },
          r: { a: 0, k: 3 },
          nm: 'reflection line 1'
        },
        {
          ty: 'rc',
          s: { a: 0, k: [6, 142] },
          p: { a: 0, k: [0, 0] },
          r: { a: 0, k: 3 },
          nm: 'reflection line 2'
        },
        {
          ty: 'fl',
          c: { a: 0, k: [1, 1, 1, 1] },
          o: { a: 0, k: 6 }, // highly transparent white reflection
          nm: 'reflection fill'
        }
      ],
      ip: 0,
      op: 90,
      st: 0,
      bm: 0
    },
    // 4. Center Label Rim (Thin accent border)
    {
      ddd: 0,
      ind: 6,
      ty: 4,
      nm: 'center rim',
      sr: 1,
      ks: transform({
        x: 90,
        y: 90,
        scale: [100, 100, 100]
      }),
      ao: 0,
      shapes: [
        { ty: 'el', p: { a: 0, k: [0, 0] }, s: { a: 0, k: [56, 56] }, nm: 'rim circle' },
        { ty: 'st', c: { a: 0, k: [0.95, 0.41, 0.11, 1] }, o: { a: 0, k: 70 }, w: { a: 0, k: 2 }, nm: 'rim stroke' }
      ],
      ip: 0,
      op: 90,
      st: 0,
      bm: 0
    },
    // 5. Center Label Fill (Pulsing vinyl label)
    {
      ddd: 0,
      ind: 7,
      ty: 4,
      nm: 'center label',
      sr: 1,
      ks: transform({
        x: 90,
        y: 90,
        scale: [
          { t: 0, s: [96, 96, 100], e: [104, 104, 100], ...ease3D },
          { t: 45, s: [104, 104, 100], e: [96, 96, 100], ...ease3D },
          { t: 90, s: [96, 96, 100] }
        ]
      }),
      ao: 0,
      shapes: [
        { ty: 'el', p: { a: 0, k: [0, 0] }, s: { a: 0, k: [46, 46] }, nm: 'label circle' },
        { ty: 'fl', c: { a: 0, k: [0.97, 0.89, 0.77, 1] }, o: { a: 0, k: 100 }, nm: 'label fill' }
      ],
      ip: 0,
      op: 90,
      st: 0,
      bm: 0
    },
    // 6. Record Center Spindle Hole (Pure black center)
    {
      ddd: 0,
      ind: 8,
      ty: 4,
      nm: 'spindle hole',
      sr: 1,
      ks: transform({
        x: 90,
        y: 90,
        scale: [100, 100, 100]
      }),
      ao: 0,
      shapes: [
        { ty: 'el', p: { a: 0, k: [0, 0] }, s: { a: 0, k: [10, 10] }, nm: 'spindle circle' },
        { ty: 'fl', c: { a: 0, k: [0.03, 0.03, 0.03, 1] }, o: { a: 0, k: 100 }, nm: 'spindle fill' }
      ],
      ip: 0,
      op: 90,
      st: 0,
      bm: 0
    }
  ]
};
