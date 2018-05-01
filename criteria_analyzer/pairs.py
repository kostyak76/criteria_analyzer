class Analyzer(object):
    """
    distributes 100% among criterias depending on user responses

    uses:
        from criteria_analyzer import Analyzer
        criterias = ['a', 'b', 'c']
        Analyzer.from_criterias(criterias).print_matrix()
    """
    def __init__(self, criterias, pair_factory, rater):
        """
        :type criterias list
        :type pair_factory PairGenerator
        :type rater Rater
        """
        super().__init__()
        self._criterias = criterias
        self._pair_factory = pair_factory
        self._rater = rater

    @classmethod
    def from_criterias(cls, criterias):
        return cls(criterias,
                   PairGenerator(criterias),
                   Rater())

    def _rate_criteria(self):
        for pair in self._pair_factory.get_pairs():
            self._rater.rate_pair(pair)

    def get_values(self):
        """
        :return: CriteriaValue generator
        """
        self._rate_criteria()
        rates = self._rater.get_rates()
        for name in self._criterias:
            yield CriteriaValue(name, rates.get(name, 0))

    def print_matrix(self):
        values = self.get_values()
        first_rate = True
        for criteria_value in values:
            if first_rate:
                first_rate = False
                print('Rate is: \n')
            print('{0.name}: %{0.value}'.format(criteria_value))


class CriteriaValue(object):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value


class PairGenerator(object):
    """
    creates pair generator from specified elements
    """
    def __init__(self, elements):
        """
        :type elements list
        """
        super().__init__()
        assert isinstance(elements, list), 'Elements should be a list'
        self._elements = elements

    def get_pairs(self):
        """
        :return: list of two elements
        """
        k = len(self._elements)
        for i in range(pow(2, k) - 1):
            # get all possible combinations
            may_be_pair = self._get_elements_by_bin_map(self._get_bin_map_of_number(i, k))
            if len(may_be_pair) == 2:
                yield may_be_pair

    def _get_elements_by_bin_map(self, bin_map):
        """
        parses map and returns all elements found on places where map has '1'(s)
        :type bin_map str
        :return:
        """
        result = []
        indexes = range(len(bin_map))
        for index, m_str in zip(indexes, bin_map):
            if int(m_str) == 1:
                result.append(self._elements[index])
        return result

    @staticmethod
    def _get_bin_map_of_number(number, length):
        """
        creates string of specified length,
        where last chars are from bin(number) and first chars just '0'
        :param number:
        :param length:
        :return:
        """
        empty_map = '0' * length
        bin_map_long = empty_map + str(bin(number))[2:]
        return bin_map_long[-length:]


class Rater(object):
    """
    rates pairs and prints result
    """
    def __init__(self):
        super(Rater, self).__init__()
        self._times = 0
        self._rates = {}

    def rate_pair(self, pair):
        """
        :type pair list
        :param pair:
        :return:
        """
        try:
            rate = input('What is better: {0}, select 1 or 2? \n'.format(pair))
            assert rate in ['1', '2'], 'Wrong selection try again'
        except AssertionError:
            print('It is wrong response. \nTry again\n')
            return self.rate_pair(pair)
        else:
            selected = pair[int(rate) -1]
            self._rates.setdefault(selected, 0)
            self._rates[selected] += 1
            self._times += 1

    def get_rates(self):
        """
        :return: dictionary of criteria_name and its rate
        """
        for key, value in self._rates.items():
            self._rates[key] = 100 * value / self._times
        return self._rates
