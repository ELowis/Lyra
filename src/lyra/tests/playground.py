#####################
# Liveness Analyses #
#####################

# from lyra.engine.liveness.liveness_analysis import LivenessAnalysis
# LivenessAnalysis().main("liveness/example.py")

# from lyra.engine.liveness.liveness_analysis import StrongLivenessAnalysis
# StrongLivenessAnalysis().main("liveness/example.py")

##################
# Usage Analyses #
##################

# from lyra.engine.usage.usage_analysis import SimpleUsageAnalysis
# SimpleUsageAnalysis().main("usage/example.py")

# from lyra.engine.usage.fulara_usage_analysis import FularaUsageAnalysis
# FularaUsageAnalysis().main("usage/running_example.py")

######################
# Numerical Analyses #
######################

# from lyra.engine.numerical.sign_analysis import ForwardSignAnalysis
# ForwardSignAnalysis().main("numerical/backward/example.py")

# from lyra.engine.numerical.sign_analysis import BackwardSignAnalysis
# BackwardSignAnalysis().main("numerical/backward/example.py")

# from lyra.engine.numerical.interval_analysis import ForwardIntervalAnalysis
# ForwardIntervalAnalysis().main("numerical/forward/example.py")

# from lyra.engine.numerical.interval_analysis import BackwardIntervalAnalysis
# BackwardIntervalAnalysis().main("numerical/backward/example.py")

from lyra.engine.container.fulara.fulara_analysis import FularaAnalysis
FularaAnalysis().main("usage/running_example.py")

###################
# String Analyses #
###################

# from lyra.engine.string.character_analysis import ForwardCharacterAnalysis
# ForwardCharacterAnalysis().main("assumption/example.py")

# from lyra.engine.string.character_analysis import BackwardCharacterAnalysis
# BackwardCharacterAnalysis().main("assumption/example.py")

##################################
# Input Data Assumption Analyses #
##################################

# from lyra.engine.assumption.assumption_analysis import TypeAnalysis
# TypeAnalysis().main("assumption/example.py")

# from lyra.engine.assumption.assumption_analysis import RangeAnalysis
# RangeAnalysis().main("assumption/example.py")

# from lyra.engine.assumption.assumption_analysis import AlphabetAnalysis
# AlphabetAnalysis().main("assumption/example.py")

# from lyra.engine.assumption.assumption_analysis import TypeQuantityAssumptionAnalysis
# TypeQuantityAssumptionAnalysis().main("assumption/example.py")

# from lyra.engine.assumption.assumption_analysis import TypeRangeAssumptionAnalysis
# TypeRangeAssumptionAnalysis().main("assumption/example.py")

# from lyra.engine.assumption.assumption_analysis import TypeAlphabetAssumptionAnalysis
# TypeAlphabetAssumptionAnalysis().main("assumption/example.py")

# from lyra.engine.assumption.assumption_analysis import TypeRangeAlphabetAssumptionAnalysis
# TypeRangeAlphabetAssumptionAnalysis().main("assumption/example.py")