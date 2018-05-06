# Skippy

## Prerequisites
```
sudo pip3 install python-vxi11
sudo pip3 install anytree
sudo pip3 install readline
```

## Basic usage
```
./skippy.py <my_vxi11_device>
```

You can use the `<TAB>` key for autocompletion inside the program. Currently, this works for a handful of commands marked as mandatory in the [SCPI-99](http://www.ivifoundation.org/docs/scpi-99.pdf) standards document.

## References
- [SCPI (Wikipedia)](https://en.wikipedia.org/wiki/Standard_Commands_for_Programmable_Instruments)
- [Python VXI-11](https://github.com/python-ivi/python-vxi11)
