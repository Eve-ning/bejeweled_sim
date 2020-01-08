# Bejeweled Simulator

## Preface
This simulates match-3 games, I'm going to use this library built in **Python** to conduct some analytics on this

# Building the Library

## Building the Board
### Linked Class Method
The first thought I had was to have each Gem's coordinates be relative to each other, that is, each `Gem` had `up()` `down()` `left()` `right()` methods that retrieves their corresponding `Gem`.

This was an interesting idea and seems to be useful to make the `Gem` fall due to gravity by replacing `down()`'s `Gem` with its own. This also seem to help in finding matches by finding which `up() and down()` or `left() and right()` matches.

In the end, I didn't use this method since it feels low-level and very memory heavy when it comes to implementing flexible algorithms!

### 2D Array Method
This was more elementary but it helps a lot in making everything simple. Accessing each row and column was more straightforward than starting from `0,0` then going to `x,y` by doing a for loop

While it does make some algorithms a bit more roundabout, it makes understanding the algorithm easier.

## Detecting Matches
To detect matches on the board, we use a `3x1` viewer that slides around the board that finds `id` matches. This doesn't count how many gems are there in a match since a `4x1` gem match would be detected twice

```
AAAA would be detected as [AAA]A & A[AAA]
```
This makes counting the gems matched incorrect!

### Marking
Instead of counting directly, we will `mark` each `Gem` if they do happen to match. In the `Gem` class, there's a `mark` attribute which is just a simple T/F flag.

Consider the following:

```
Board IDs
| | - + 
+ + + + 
+ | | | 
+ | - | 

Board Marks (O = True, X = False)
X X X X 
O O O O 
O O O O 
O X X X 
```

Notice how the viewer can just slide around and mark those that are valid.

## Counting Matches
To do this, we will loop through every **marked** gem and *crawl* through the board to find the maximum cluster.

For example, starting from the first marked gem in the example

```
 | | - +     X X X X  Count 1
[+]+ + +    [X]O O O  ID '+'
 + | | |     O O O O 
 + + + |     O O O X 
```

Firsltly, it will **unmark** the selected `Gem`
The algorithm will crawl in 1 direction, let's say to the right.
It will only crawl if the **ID matches** and **is marked**

```
 | | - +     X X X X  Count 4
[+ + + +]   [X X X X] ID '+'
 + | | |     O O O O
 + + + |     O O O X
```

The algorithm will **unmark** every visited `Gem`
Then the algorithm will be used on every visited `Gem`

```
 | | - +     X X X X  Count 6
[+ + + +]   [X X X X] ID '+'
[+]| | |    [X]O O O
[+]+ + |    [X]O O X
```

This will occur until there are no more "crawlable" `Gem`

```
 | | - +     X X X X  Count 8
[+ + + +]   [X X X X] ID '+'
[+]| | |    [X]O O O
[+ + +]|    [X X X]X
```

Then the algorithm will output a list whereby `[[id, x, y, count], ...]`, x and y is the first visited `Gem`.

### Discrepency
Notice that this may not be consistent with some other games where

```
| + + +
+ + + |
```
Is counted as two `3 Matches`. In our case, it's a `6 Match`. If we were to use their algorithm, we can implement a sliding viewer for different types such as
```
  o   | o o o | o     |
o o o | o     | o     | etc.
  o   | o     | o o o |
```
This would be more computationally expensive for viewer sliding


