## --- LDAP Server --- ##

nhqb-vm-2:
pass: ubuntu

## --- Instllation --- ##

sudo apt install slapd ldap-utils

## --- Configuration --- ##

sudo dpkg-reconfigure slapd

## --- Testing --- ##

ldapsearch -x -LLL -H ldap:/// -b dc=example,dc=com dn

## --- User --- ##

```bash
nano base.ldif

    dn: ou=users,dc=example,dc=com
    objectClass: organizationalUnit
    ou: users

    dn: ou=groups,dc=example,dc=com
    objectClass: organizationalUnit
    ou: groups
```

```bash
    sudo ldapadd -x -D cn=admin,dc=example,dc=com -W -f base.ldif
```

## --- Update slappasswd --- ##

```bash
    slappasswd
```

```bash
    nano update_rootpw.ldif

    dn: olcDatabase={1}mdb,cn=config
    changetype: modify
    replace: olcRootPW
    olcRootPW: {SSHA}password
```

```bash
    ldapmodify -Y EXTERNAL -H ldapi:/// -f update_rootpw.ldif
```

## --- Check --- ##

```bash
     ldapsearch -x -H ldap://localhost -D "cn=admin,dc=example,dc=com" -w ubuntu -b "ou=users,dc=example,dc=com" "(uid=baonguyen3197)"
```