<?php
// Starting numbers are 0 and 1
    function fibonnaci($n) {
        if($n == 0) {
            return $n;
        } elseif($n == 1) {
            return $n;
        } else {
            return fibonnaci($n-2) + fibonnaci($n-1); 
        }
    }

echo fibonnaci(6);
?>