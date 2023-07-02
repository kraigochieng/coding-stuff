<?php 
    function tribonacci($n) {
        if($n == 0) {
            return 0;
        } elseif ($n == 1 || $n == 2) {
            return 1;
        } elseif ($n == 3) {
            return 2;
        } else {
            return tribonacci($n-1) + tribonacci($n-2) + tribonacci($n-3);
        }
    }

    echo tribonacci(4);
?>