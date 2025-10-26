from typing import Any, Callable, Iterable, List, Mapping, Optional, Sequence, Union, Tuple  # import types for annotations and clarity
Key = Union[str, Callable[[Mapping[str, Any]], Any]]  # define a type alias for the key parameter meaning

def _get_by_key(item: Mapping[str, Any], key: Key) -> Any:  # helper to extract value by key or callable
    if callable(key):  # if key is a callable function
        return key(item)  # call it with the item and return the result
    parts = key.split(".")  # support nested keys using dot notation by splitting on '.'
    val: Any = item  # start traversal from the top-level item
    for p in parts:  # iterate over each part of the nested path
        if not isinstance(val, Mapping) or p not in val:  # if current value isn't a mapping or part missing
            raise KeyError(p)  # indicate the key part was not found
        val = val[p]  # descend into the mapping for the next part
    return val  # return the final extracted value

def sort_dicts(  # main sorting function definition
    items: Iterable[Mapping[str, Any]],  # iterable of dict-like objects to sort
    key: Key,  # key can be a string (optionally dot-separated) or a callable
    reverse: bool = False,  # whether to sort in descending order when True
    missing: Union[str, Any] = "last",  # handling for items missing the key: "last", "first", "raise", or a fill value
) -> List[Mapping[str, Any]]:  # returns a new list of mapping objects sorted accordingly
    present: List[Tuple[Any, Mapping[str, Any]]] = []  # list to hold (extracted_value, item) for items that have the key
    missing_items: List[Mapping[str, Any]] = []  # list to hold items missing the key when placed first/last

    for it in items:  # iterate over each item provided
        try:  # attempt to extract the value for sorting
            val = _get_by_key(it, key)  # use helper to get the value or raise KeyError
            present.append((val, it))  # store the value and item together for stable sorting
        except KeyError:  # handle the case where the key is missing
            if missing == "raise":  # if configured to raise on missing keys
                raise  # re-raise the KeyError to signal the caller
            elif missing in ("last", "first"):  # if configured to put missing items first or last
                missing_items.append(it)  # collect missing items separately for later placement
            else:  # otherwise treat `missing` as a fill value to include in the normal sort
                present.append((missing, it))  # insert the fill value so missing items are sorted with others

    present.sort(key=lambda pair: pair[0], reverse=reverse)  # sort the present list by the extracted value, respecting reverse
    sorted_present = [pair[1] for pair in present]  # extract the original items in sorted order from the (value, item) pairs

    if missing == "last":  # if missing items should be placed at the end
        return sorted_present + missing_items  # return sorted items followed by missing items
    elif missing == "first":  # if missing items should be placed at the start
        return missing_items + sorted_present  # return missing items first and then the sorted items
    else:  # missing was a custom fill value (or other non-"first"/"last"/"raise" value)
        return sorted_present  # already included missing items in present, so just return the sorted list

if __name__ == "__main__":  # example usage when running this file directly
    data = [  # sample list of dictionaries to demonstrate behavior
        {"name": "alice", "age": 30},  # item with an age
        {"name": "bob"},  # item missing age
        {"name": "carol", "age": 25},  # item with a younger age
    ]  # end of sample data list

    print(sort_dicts(data, "age"))  # default: sort ascending by 'age', missing items go last
    print(sort_dicts(data, "age", reverse=True, missing="first"))  # sort descending, missing items placed first
    print(sort_dicts(data, lambda d: d.get("name")))  # use a callable key to sort by name
    nested = [  # sample demonstrating nested key support
        {"id": 1, "address": {"city": "Seattle"}},  # has nested address.city
        {"id": 2},  # missing nested address
        {"id": 3, "address": {"city": "Austin"}},  # has nested address.city
    ]  # end nested sample

    print(sort_dicts(nested, "address.city", missing="last"))  # sort by nested key, missing placed last