class Error(Exception):
    """Classse base para outras exceções"""
    pass


class RulesListEmpty(Error):
    """Exceção chamada quando a lista das regras está vazia"""
    pass


class NoMovieFound(Error):
    """Exceção chamada quando não existe um determinado filme"""
    pass


class NoItemRecommended(Error):
    """Exceção chamada quando não existe nenhum item a ser recomendado"""
    pass
