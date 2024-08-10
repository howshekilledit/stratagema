# Notes

When ever a create a new repo I should do `notes.md`, `README.md`, `LICENSE.md` and `.gitignore`. 

## August 10, 2024

Have been working on this for weeks now, and spent probably a full day stuck on the question of why I couldn't create a tree where all branches end in a goal. This is what I got from a recursion algorithm that did not explore any duplicate state-action pairs: 

![image-20240810110217558](/Users/mgreen/Library/Application Support/typora-user-images/image-20240810110217558.png)

and this is what I got when I tried to go back in and duplicate the branches that led to goals for states-actions that had already been explored: 

![image-20240810110313556](/Users/mgreen/Library/Application Support/typora-user-images/image-20240810110313556.png)

and only today did I realize that I should just be stripping away all branches that don't lead to goals 

![image-20240810110422116](/Users/mgreen/Library/Application Support/typora-user-images/image-20240810110422116.png)

(used a different positioning algorithm for this one)

On the other hand the convoluted trees have their own beauty... i'm still interested in solving my earlier question but probbaly not for pedagogical purposes. 