# FileSystem

## Protocol Hierarchy

```text
DiskRepresentable
├── Movable
├── Copyable
└── Readable
    └── Writeable
```

## Class Hierarchy

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