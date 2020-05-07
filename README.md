# lmp2cfg.py
To convert lammps dump file to atomeye cfg file.

Lammps: https://lammps.sandia.gov/

Atomeye: http://li.mit.edu/Archive/Graphics/A/

![lmp2cfg.py](https://github.com/kyphd/lmp2cfg.py/blob/master/images/lmp2cfg.png)

## Table of Contents

* [What is lmp2cfg.py?](#what-is-lmp2cfg.py)
* [How to Use](#how-to-use)
* [Contributing](#contributing)
* [Authors](#authors)
* [License](#license)

## What is lmp2cfg.py?

lmp2cfg.py is to convert lammps dump file to atomeye cfg file. 
Lammps has "dump cfg" command, so this app is not important. 
However, if you forget to dump cfg file, you can convert dump file to cfg file after MD calculation.
Lammps tool also has lmp2cfg.f, lmp2cfg.f require to make an input file.
lmp2cfg.py ask you the necessary parameter after execution and you don't need to prepare any files.

## How to Use

### 1. Execute lmp2cfg.py

~~~
$ python lmp2cfg.py <dump file>
~~~

Coordinate of each atom (\[x, y, z\] or \[xs, ys zs\]) and type arguments are required in dump file.

Generally, "dump atom" command outputs all of them.

### 2. You are asked the mass and element for each atom type in dump file.

ex.

~~~
1 atom types are found. Input mass and element for each atom type.
For #1
 mass: 55.85
 element: Fe
~~~

### 3. CFG file will be generated.

## Contributing

1. Fork this
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

## Authors

* **K. Yabuuchi** 
* See also the list of [contributors](https://github.com/kyphd/lmp2cfg.py/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details