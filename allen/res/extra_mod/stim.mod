COMMENT
Since this is an synapse current, positive values of i depolarize the cell
and is a transmembrane current.
ENDCOMMENT

NEURON {
	POINT_PROCESS ISyn
	RANGE delay, dur, amp, i
	NONSPECIFIC_CURRENT i
}
UNITS {
	(nA) = (nanoamp)
}

PARAMETER {
	delay (ms)
	dur (ms)	<0,1e9>
	amp (nA)
}
ASSIGNED { i (nA) }

INITIAL {
	i = 0
}

BREAKPOINT {
	at_time(delay)
	at_time(delay+dur)
	if (t < delay + dur && t >= delay) {
		i = -amp
	}else{
		i = 0
	}
}
