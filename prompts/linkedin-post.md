Draft the next LinkedIn post from docs/POSTS.md.

1. Take the first row whose date is today or past and whose post isn't in posts/ yet.
2. Check its gate. For every number in the hook, find the file it comes from on the Spark
   (`bin/jz run "cd <repo> && cat <file>"`). If the gate isn't met, say what is missing and stop.
3. Write posts/<date>-<project>.md:
   - the post: a hook line, then 3-5 short lines, then one line of what's next;
   - the first comment (the repo link);
   - the visual to attach, and where it is;
   - a "Sources" list of each number and its file.
   Write plainly in Jehanzeb's voice, first person. No hype words, no emoji walls, no hashtag
   blocks (at most 3 hashtags).
4. Follow the rules at the bottom of docs/POSTS.md. Commit the draft. Never post anything.
