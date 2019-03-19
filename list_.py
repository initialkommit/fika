def chunks(li, chunk_size):
    """list를 chunk_size로 잘라서 반환한다.

    Return:
        yield
    """
    if len(li) < 1 or chunk_size < 1:
        return li

    chunk_size = int(chunk_size)
    for i in range(0, len(li), chunk_size):
        yield li[i: i + chunk_size]


def chunkify(li, max_split):
    """주어진 List를 max_split 수대로 자른다.

    Parameters:
        li: Split 대상 List
        max_split: Split 수

    Return:
        Lists in list
    """
    min_chunk_size = len(li) // max_split
    max_chunk_size = min_chunk_size + 1

    if min_chunk_size == 0:
        return li
    max_chunk_split = len(li) % max_split
    min_chunk_split = max_split - max_chunk_split

    li2 = []
    li2.extend(list(chunks(
        li[:min_chunk_size * min_chunk_split], min_chunk_size)))
    li2.extend(list(chunks(
        li[min_chunk_size * min_chunk_split:], max_chunk_size)))

    return li2

