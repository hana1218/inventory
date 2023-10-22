# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
from datetime import date, timedelta
import random
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate
from service.models import Inventory, Condition


class ProductFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Inventory

    id = factory.LazyFunction(lambda: random.randint(0, 200))
    name = factory.Faker("first_name")
    quantity = factory.LazyFunction(lambda: random.randint(0, 1000))
    restock_level = factory.LazyFunction(lambda: random.randint(0, 50))
    restock_count = factory.LazyFunction(lambda: random.randint(50, 200))
    condition = FuzzyChoice(choices=[Condition.NEW, Condition.OPEN_BOX, Condition.USED])
    first_entry_date = FuzzyDate(date(2008, 1, 1))
    last_restock_date = factory.LazyAttribute(
        lambda t: t.first_entry_date + timedelta(days=random.randint(1, 365))
    )
