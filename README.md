# GIF to Sphero Animation

The Sphero BOLT (codenamed "Polaris") has an 8x8 RGB LED matrix. Sphero EDU allows you to program Sphero robots with JavaScript, and allows you to define animations for BOLT's matrix. Specifically, the format is as follows:

```js
async function startProgram() {
  playMatrixAnimation(0);
}

registerMatrixAnimation({
  frames: [
    [
      [1, 1, 6, 6, 6, 6, 1, 1],
      [1, 6, 6, 6, 6, 6, 6, 1],
      [6, 6, 1, 6, 6, 1, 6, 6],
      [6, 6, 6, 6, 6, 6, 6, 6],
      [6, 6, 6, 1, 1, 6, 6, 6],
      [6, 6, 6, 1, 1, 6, 6, 6],
      [1, 6, 6, 6, 6, 6, 6, 1],
      [1, 1, 6, 6, 6, 6, 1, 1],
    ],
    [
      [6, 6, 6, 6, 6, 6, 6, 6],
      [6, 6, 1, 6, 6, 1, 6, 6],
      [6, 6, 1, 6, 6, 1, 6, 6],
      [6, 1, 1, 6, 6, 1, 1, 6],
      [6, 6, 6, 6, 6, 6, 6, 6],
      [6, 1, 1, 1, 1, 1, 1, 6],
      [1, 6, 1, 1, 1, 1, 6, 1],
      [1, 1, 6, 6, 6, 6, 1, 1],
    ],
  ],
  palette: [
    { r: 255, g: 255, b: 255 },
    { r: 0, g: 0, b: 0 },
    { r: 255, g: 0, b: 0 },
    { r: 255, g: 16, b: 0 },
    { r: 255, g: 128, b: 0 },
    { r: 255, g: 191, b: 0 },
    { r: 255, g: 255, b: 0 },
    { r: 185, g: 246, b: 30 },
    { r: 0, g: 255, b: 0 },
    { r: 185, g: 255, b: 255 },
    { r: 0, g: 255, b: 255 },
    { r: 0, g: 0, b: 255 },
    { r: 145, g: 0, b: 211 },
    { r: 157, g: 48, b: 118 },
    { r: 255, g: 0, b: 255 },
    { r: 204, g: 27, b: 126 },
  ],
  fps: 6,
  transition: MatrixAnimationTransition.None,
});
```

Which defines the following animation:

![2 Frame Animation by the Sphero EDU Docs](https://lh6.googleusercontent.com/r-VhXPHJVBNOawGemQ7POna9TYLYMX_v-Kn8ryMLEUsYHcCgR4XC6Y7-idZe6buRajwBRi5VTMr41dvAG6nXKl-_kHDxXpDWox4rh7vXUJ1M0MiIK2WQ2JaKuR2Joh08WQ=w1280)

The numbers within the arrays acts as an accessor for the pallet array. Otherwise, each array within the frame defines an array of pixels to set sequentially across the x axis.

This script takes in a path to a GIF and will spit out a JSON files with a max of 600 frames each in the current working directory in the format of `sphero-animation-{{unixtime}}-{{segment}}.json`.

Currently, it cannot compress the GIF, so it will only pull an 8x8 area of the top-left, and the first 16 colors. I strongly recommend pre-processing the GIF to meet these requirements. In the future, this should be handled automatically. (Feel free to make a PR if you're impatient. :3) You will also have to set the transition.
