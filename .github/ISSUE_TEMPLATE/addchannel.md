---
name: addchannel
about: Request an addition to the playlist.
title: "[Add a new channel]"
labels: add stream
assignees: ''

---

- type: input
    id: name
    attributes:
      label: Channel name
      description: Name of the channel goes here.
      placeholder: ex. Shalini TV
    validations:
      required: true
- type: input
  id: region
  attributes:
    label: Channel region
    description: Region in which the channel belongs to. (Use '~' if the region is unknown)
    placeholder: ex. Kanchipuram
  validations:
    required: true
- type: dropdown
  id: category
  attributes:
    label: Channel category
    description: Category in which the channel belongs to. (Default is PLC)
    multiple: false
    options:
      - PLC
      - Movies
      - Music
      - Classic
      - Lifestyle
      - News
      - Hindu Devotional
      - Islamic Devotional
      - Christian Devotional
    default: 0
  validations:
    required: true
- type: input
  id: logo
  attributes:
    label: Channel logo
    description: URL of the logo of the channel.
  validations:
    required: false
- type: input
  id: link
  attributes:
    label: Channel link
    description: Link to the stream of the channel.
    placeholder: ex. http://103.78.164.62:8090/SHALINITVHD/index.m3u8
  validations:
    required: true
- type: textarea
   id: notes
   attributes:
       label: Notes
       description: Additional notes 
       render: shell
