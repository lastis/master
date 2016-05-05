import LFPy

def get_cell(neuron_name):
    """
    Load a spesific model based on the input string and return 
    a LFPy Cell object

    :param string neuron_name: 
        String to identify the neuron model that will be loaded.
    :returns: 
        Cell object from LFPy. 
    """

    cell = LFPy.Cell( some cell parameters ... )

    return cell
