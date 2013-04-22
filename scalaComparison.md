####Simple Scala tests to compare to python in the format of the included python

Seems to have the same results as python: values can be accessed but not modified by inner scoped functions. 

<br>
Testing with Var:

<pre><code>
    def AccessWithVar(): Int ={
      var count = 0
      def counter() =
	count + 1
      counter()
    }

</pre></code>  
works fine<br><br>
Testing with Val:

<pre><code>`   
    def AccessWithVal(): Int ={
      val count = 0 
      def counter() =
	count + 1
      counter()
    }

</pre></code> 

also works <br><br>
Testing ability to modify from an innerscope:		   

<pre><code> 
    def ModifyWithVar(): Int ={
      var count = 0 
      def counter() =
	count+=1
      counter()
    }

</pre></code> 
throws an error because it is modifying- returns:

<pre><code> 
 <console>:13: error: type mismatch;
 found   : Unit
 required: Int
             counter()
</pre></code> 
`
