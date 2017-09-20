# AudioDiag

I'm honestly just making this as a simple tool to use instead of SMAART\n
The goal behind this is to keep things incredibly simple:\n
\n
You'll have a left pane where you choose\n
\t  the input signal, idealing a flat response mic that is measuring the room\n
\t  the output signal, which will be the output from this program giving you things like noise and tone\n
\t  the reference signal, ideally a matrix of the mains from your board. Eventually, I'll optionally link this to the output\n
  \n\n
On the right side you'll have a slew of plots:\n
\t  The live response RTA of the input (right now I have RTA and waveform, but that's more for testing)\n
\t\t    Eventually this will be more of a contour graph that shows the ~5-10s history of the RTA\n
\t  The phase differences of input and reference. This should be used to fix delay times when using multiple speakers\n
\t  The live coherence response (again this will be eventually more of a rolling contour plot showing 5-10s of history)\n
\t  And finally the RTA mean differences (running mean over RTA history) in dB\n
\t  Below this will be a "Minimize Cost?" which will run an analysis. More on this in a sec*\n
\t\t    there will be an option to specifiy geq corrections and peq corrections (with and without modular q)\n
 \t\t   *What this will do is run a highly costly function on your computer \n
 \t\t     and compute the suggested adjustments to make on your geq and peq\n
      
  
