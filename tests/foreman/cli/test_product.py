# -*- encoding: utf-8 -*-
"""Test class for Product CLI"""
import time

from fauxfactory import gen_alphanumeric, gen_string
from robottelo.cli.base import CLIReturnCodeError
from robottelo.cli.factory import (
    CLIFactoryError,
    make_gpg_key,
    make_org,
    make_product,
    make_repository,
    make_sync_plan,
)
from robottelo.cli.product import Product
from robottelo.datafactory import (
    generate_strings_list,
    valid_data_list,
    valid_labels_list,
    invalid_values_list,
)
from robottelo.decorators import bz_bug_is_open, run_only_on, tier1, tier2
from robottelo.test import CLITestCase


class ProductTestCase(CLITestCase):
    """Product CLI tests."""

    org = None

    # pylint: disable=unexpected-keyword-arg
    def setUp(self):
        """Tests for Lifecycle Environment via Hammer CLI"""

        super(ProductTestCase, self).setUp()

        if ProductTestCase.org is None:
            ProductTestCase.org = make_org(cached=True)

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_name(self):
        """Check if product can be created with random names

        @Feature: Product

        @Assert: Product is created and has random name
        """
        for name in valid_data_list():
            with self.subTest(name):
                product = make_product({
                    u'name': name,
                    u'organization-id': self.org['id'],
                })
                self.assertEqual(product['name'], name)
                self.assertGreater(len(product['label']), 0)

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_label(self):
        """Check if product can be created with random labels

        @Feature: Product

        @Assert: Product is created and has random label
        """
        for label in valid_labels_list():
            with self.subTest(label):
                product_name = gen_alphanumeric()
                product = make_product({
                    u'label': label,
                    u'name': product_name,
                    u'organization-id': self.org['id'],
                })
                self.assertEqual(product['name'], product_name)
                self.assertEqual(product['label'], label)

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_description(self):
        """Check if product can be created with random description

        @Feature: Product

        @Assert: Product is created and has random description
        """
        for desc in valid_data_list():
            with self.subTest(desc):
                product_name = gen_alphanumeric()
                product = make_product({
                    u'description': desc,
                    u'name': product_name,
                    u'organization-id': self.org['id'],
                })
                self.assertEqual(product['name'], product_name)
                self.assertEqual(product['description'], desc)

    @tier1
    def test_positive_create_with_gpg_key(self):
        """Check if product can be created with gpg key

        @Feature: Product

        @Assert: Product is created and has gpg key
        """
        gpg_key = make_gpg_key({u'organization-id': self.org['id']})
        for name in valid_data_list():
            with self.subTest(name):
                product = make_product({
                    u'gpg-key-id': gpg_key['id'],
                    u'name': name,
                    u'organization-id': self.org['id'],
                })
                self.assertEqual(product['name'], name)
                self.assertEqual(product['gpg']['gpg-key-id'], gpg_key['id'])

    @tier1
    def test_positive_create_with_sync_plan(self):
        """Check if product can be created with sync plan

        @Feature: Product

        @Assert: Product is created and has random sync plan
        """
        sync_plan = make_sync_plan({
            u'organization-id': self.org['id']
        })
        for name in valid_data_list():
            with self.subTest(name):
                product = make_product({
                    u'name': name,
                    u'organization-id': self.org['id'],
                    u'sync-plan-id': sync_plan['id'],
                })
                self.assertEqual(product['name'], name)
                self.assertEqual(product['sync-plan-id'], sync_plan['id'])

    @tier1
    def test_negative_create_with_name(self):
        """Check that only valid names can be used

        @Feature: Product

        @Assert: Product is not created
        """
        for invalid_name in invalid_values_list():
            with self.subTest(invalid_name):
                with self.assertRaises(CLIFactoryError):
                    make_product({
                        u'name': invalid_name,
                        u'organization-id': self.org['id'],
                    })

    @tier1
    def test_negative_create_with_label(self):
        """Check that only valid labels can be used

        @Feature: Product

        @Assert: Product is not created
        """
        product_name = gen_alphanumeric()
        for invalid_label in (gen_string('latin1', 15), gen_string('utf8', 15),
                              gen_string('html', 15)):
            with self.subTest(invalid_label):
                with self.assertRaises(CLIFactoryError):
                    make_product({
                        u'label': invalid_label,
                        u'name': product_name,
                        u'organization-id': self.org['id'],
                    })

    @tier1
    def test_positive_update_description(self):
        """Update the description of a product

        @Feature: Product

        @Assert: Product description is updated
        """
        product = make_product({u'organization-id': self.org['id']})
        for desc in valid_data_list():
            with self.subTest(desc):
                Product.update({
                    u'description': desc,
                    u'id': product['id'],
                })
                result = Product.info({
                    u'id': product['id'],
                    u'organization-id': self.org['id'],
                })
                self.assertEqual(result['description'], desc)

    @run_only_on('sat')
    @tier1
    def test_positive_update_gpg_key(self):
        """Update product's gpg keys

        @Feature: Product

        @Assert: Product gpg key is updated
        """
        first_gpg_key = make_gpg_key({u'organization-id': self.org['id']})
        second_gpg_key = make_gpg_key({u'organization-id': self.org['id']})
        product = make_product({
            u'gpg-key-id': first_gpg_key['id'],
            u'organization-id': self.org['id'],
        })
        # Update the Descriptions
        Product.update({
            u'gpg-key-id': second_gpg_key['id'],
            u'id': product['id'],
        })
        # Fetch it
        product = Product.info({
            u'id': product['id'],
            u'organization-id': self.org['id'],
        })
        self.assertEqual(product['gpg']['gpg-key-id'], second_gpg_key['id'])
        self.assertNotEqual(product['gpg']['gpg-key-id'], first_gpg_key['id'])

    @run_only_on('sat')
    @tier1
    def test_positive_update_sync_plan(self):
        """Update product's sync plan

        @Feature: Product

        @Assert: Product sync plan is updated
        """
        first_sync_plan = make_sync_plan({u'organization-id': self.org['id']})
        second_sync_plan = make_sync_plan({u'organization-id': self.org['id']})
        product = make_product({
            u'organization-id': self.org['id'],
            u'sync-plan-id': first_sync_plan['id'],
        })
        # Update the Descriptions
        Product.update({
            u'id': product['id'],
            u'sync-plan-id': second_sync_plan['id'],
        })
        # Fetch it
        product = Product.info({
            u'id': product['id'],
            u'organization-id': self.org['id'],
        })
        self.assertEqual(product['sync-plan-id'], second_sync_plan['id'])
        self.assertNotEqual(product['sync-plan-id'], first_sync_plan['id'])

    @run_only_on('sat')
    @tier1
    def test_positive_update_name(self):
        """Rename Product back to original name

        @Feature: Product

        @Assert: Product Renamed to original
        """
        for prod_name in generate_strings_list():
            with self.subTest(prod_name):
                prod = make_product({
                    u'name': prod_name,
                    u'organization-id': self.org['id'],
                })
                new_prod_name = gen_string('alpha', 8)
                # Update the product name
                Product.update({
                    u'id': prod['id'],
                    u'name': new_prod_name,
                })
                # Verify Updated
                prod = Product.info({
                    u'id': prod['id'],
                    u'organization-id': self.org['id'],
                })
                self.assertEqual(prod['name'], new_prod_name)
                # Now, Rename product to original
                Product.update({
                    u'id': prod['id'],
                    u'name': prod_name,
                })
                prod = Product.info({
                    u'id': prod['id'],
                    u'organization-id': self.org['id'],
                })
                # Verify renamed back to Original name.
                self.assertEqual(prod['name'], prod_name)

    @run_only_on('sat')
    @tier1
    def test_positive_delete_by_id(self):
        """Check if product can be deleted

        @Feature: Product

        @Assert: Product is deleted
        """
        new_product = make_product({u'organization-id': self.org['id']})
        Product.delete({u'id': new_product['id']})
        with self.assertRaises(CLIReturnCodeError):
            Product.info({
                u'id': new_product['id'],
                u'organization-id': self.org['id'],
            })
            if bz_bug_is_open(1219490):
                for _ in range(5):
                    time.sleep(5)
                    Product.info({
                        u'id': new_product['id'],
                        u'organization-id': self.org['id'],
                    })

    @tier2
    def test_positive_add_sync_plan_by_id(self):
        """Check if a sync plan can be added to a product

        @Feature: Product

        @Assert: Product has sync plan
        """
        new_product = make_product({u'organization-id': self.org['id']})
        sync_plan = make_sync_plan({'organization-id': self.org['id']})
        Product.set_sync_plan({
            'id': new_product['id'],
            'sync-plan-id': sync_plan['id'],
        })
        new_product = Product.info({
            'id': new_product['id'],
            'organization-id': self.org['id'],
        })
        self.assertEqual(new_product['sync-plan-id'], sync_plan['id'])

    @tier2
    def test_positive_remove_sync_plan_by_id(self):
        """Check if a sync plan can be removed from a product

        @Feature: Product

        @Assert: Product has sync plan
        """
        product = make_product({u'organization-id': self.org['id']})
        sync_plan = make_sync_plan({'organization-id': self.org['id']})
        Product.set_sync_plan({
            'id': product['id'],
            'sync-plan-id': sync_plan['id'],
        })
        product = Product.info({
            'id': product['id'],
            'organization-id': self.org['id'],
        })
        self.assertEqual(product['sync-plan-id'], sync_plan['id'])
        Product.remove_sync_plan({'id': product['id']})
        product = Product.info({
            'id': product['id'],
            'organization-id': self.org['id'],
        })
        self.assertEqual(len(product['sync-plan-id']), 0)

    @tier2
    def test_positive_sync_by_id(self):
        """Check if product can be synchronized by its ID.

        @Feature: Product

        @Assert: Product is synchronized
        """
        org = make_org()
        product = make_product({'organization-id': org['id']})
        make_repository({'product-id': product['id']})
        Product.synchronize({
            'id': product['id'],
            'organization-id': org['id'],
        })
        product = Product.info({
            'id': product['id'],
            'organization-id': org['id'],
        })
        self.assertEqual(u'Syncing Complete.', product['sync-state'])

    @tier2
    def test_positive_sync_by_name(self):
        """Check if product can be synchronized by its name.

        @Feature: Product

        @Assert: Product is synchronized
        """
        org = make_org()
        product = make_product({'organization-id': org['id']})
        make_repository({'product-id': product['id']})
        Product.synchronize({
            'name': product['name'],
            'organization': org['name'],
        })
        product = Product.info({
            'id': product['id'],
            'organization-id': org['id'],
        })
        self.assertEqual(u'Syncing Complete.', product['sync-state'])

    @tier2
    def test_positive_sync_by_label(self):
        """Check if product can be synchronized by its label.

        @Feature: Product

        @Assert: Product is synchronized
        """
        org = make_org()
        product = make_product({'organization-id': org['id']})
        make_repository({'product-id': product['id']})
        Product.synchronize({
            'id': product['id'],
            'organization-label': org['label'],
        })
        product = Product.info({
            'id': product['id'],
            'organization-id': org['id'],
        })
        self.assertEqual(u'Syncing Complete.', product['sync-state'])
