# 🚀 Landing Zone Simulation

This project simulates alien spaceship landings on urban maps.

The goal is to determine whether each spaceship can land safely on a city map, based on building positions and the space required for opening hatches on each side.

## 🧠 Storyline

The Caponians, an alien species from a distant galaxy, plan to invade Earth.  
To do this, they’ve installed *mind bending machines* that reduce human intelligence via the telephone network.

Now, they are ready to land their ships — but they must find enough empty space in our cities.  
Each spaceship is rectangular (W x H) and requires extra space `D` on each side to open its hatches.

## 📥 Input

1. **City map**  
   A black image where:
   - Each building is a solid colored rectangle
   - Each building has a unique RGB color  
   - Rectangles are saved in a `.txt` file, one per line:  
     `x, y, w, h, r, g, b`

2. **Spaceships**  
   A list of `(W, H, D)` triplets (width, height, hatch space), in a `.txt` file  
   Triplets may be separated by any number of spaces, tabs, or line breaks.

## 📤 Output

A list of Boolean values.  
Each value is `True` if there is enough space in the city map for that spaceship to land with all 4 hatches open.

## 🖼️ Example

City map:

```
**....
**....
......
......
....++
....++
```

Spaceships:

```
(3, 3, 0)
(2, 2, 4)
```

Results:

```
[True, False]
```

Explanation:  
Only the first spaceship can land because it doesn’t require extra space for hatches (`D = 0`).  
The second one cannot land because there's no area large enough for both the ship and its hatches.

## 🔗 Reference

Inspired by:  
[Zak McKracken and the Alien Mindbenders](https://en.wikipedia.org/wiki/Zak_McKracken_and_the_Alien_Mindbenders)
