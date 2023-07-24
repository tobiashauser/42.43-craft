# Models

## Class Hierarchy

This package extends the classes from **FileSystem** to include
**Template**, **TexTemplate**, **Preamble**, **Header**, **Exercise** 
and **Templates**.

```text
Resource
├── File: Copyable, Movable
│   └── Template: Readable, Writable
│       └── TexTemplate
│           ├── Preamble
│           ├── Header
│           └── Exercise
└── Folder: Copyable, Movable
    └── Templates
```