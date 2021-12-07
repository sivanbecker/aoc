
init: aoc2021/ aoc2021/aocli.py  
ifdef day
	poetry run python aoc2021/aocli.py init --day ${day}
else
	@echo "Day not provided"
endif

test: aoc2021/ aoc2021/aocli.py 
ifdef day
ifdef part
	poetry run python aoc2021/aocli.py solve --day ${day} --part ${part} --year 2021 --test
else
	@echo "Missing part 1 or 2"
endif
else	
	@echo "Day not provided"
endif

solve: aoc2021/ aoc2021/aocli.py 
ifdef day
ifdef part
	poetry run python aoc2021/aocli.py solve --day ${day} --part ${part} --year 2021
else
	@echo "Missing part 1 or 2"
endif
else
	@echo "Day not provided"
endif